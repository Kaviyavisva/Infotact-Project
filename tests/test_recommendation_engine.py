"""
Unit tests for the Recommendation Engine module using pytest.
"""

import pytest
from src.recommendation_engine import RecommendationEngine, FinalRecommendation

@pytest.fixture
def engine():
    """Fixture to provide a clean RecommendationEngine instance."""
    return RecommendationEngine()

def test_initialization(engine):
    """Test successful initialization without an LLM client."""
    assert engine.llm_client is None

def test_analyze_chunks_valid_input(engine):
    """Test standard recommendation generation using the dynamic heuristic analyzer."""
    chunks = [
        "To replace the seal, use a 10mm wrench to unbolt the housing.",
        "Ensure the system is depressurized before beginning."
    ]
    
    rec = engine.analyze_chunks(chunks, alert_context="Hydraulic Leak Alert")
    
    assert isinstance(rec, FinalRecommendation)
    assert rec.alert_context == "Hydraulic Leak Alert"
    assert len(rec.actions) == 2  # One action generated per chunk
    
    # Verify dynamic regex extraction on the first chunk
    assert "Wrench" in rec.actions[0].required_tools
    assert "Seal" in rec.actions[0].required_parts

def test_analyze_chunks_empty_input(engine):
    """Test validation raises ValueError for completely empty inputs."""
    with pytest.raises(ValueError, match="cannot be empty or malformed"):
        engine.analyze_chunks([])

def test_analyze_chunks_whitespace_input(engine):
    """Test validation raises ValueError for whitespace-only strings."""
    with pytest.raises(ValueError, match="No valid text found"):
        engine.analyze_chunks(["   ", "", "\n"])

def test_llm_fallback_mechanism():
    """Test that the engine safely falls back to heuristic analysis if LLM fails or is unimplemented."""
    class MockLLM:
        """A simple mock class to trigger the LLM integration path."""
        pass
        
    engine_with_llm = RecommendationEngine(llm_client=MockLLM())
    
    chunks = ["Standard inspection procedure."]
    # The analyze_chunks method should attempt _generate_with_llm, catch the NotImplementedError, 
    # and successfully return the heuristic analysis instead of crashing.
    rec = engine_with_llm.analyze_chunks(chunks, "LLM Fallback Test")
    
    assert len(rec.actions) == 1
    assert "Standard inspection procedure" in rec.actions[0].issue_identified

def test_format_recommendation(engine):
    """Test that the structured dataclass formats properly into a readable string report."""
    chunks = ["Use a screwdriver to open the control panel."]
    rec = engine.analyze_chunks(chunks, "Formatting Validation")
    
    report = engine.format_recommendation(rec)
    
    # Validate the final report string
    assert isinstance(report, str)
    assert "PRESCRIPTIVE MAINTENANCE REPORT" in report
    assert "Formatting Validation" in report
    assert "Screwdriver" in report
