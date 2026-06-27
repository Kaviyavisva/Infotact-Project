"""
Recommendation Engine for the Prescriptive Maintenance RAG Agent.

This module processes retrieved maintenance manual chunks from the search engine
and synthesizes them into actionable, step-by-step prescriptive maintenance
recommendations, including required tools and spare parts.
"""

from typing import List, Optional, Any
from dataclasses import dataclass
import logging
import re

# Set up logging for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


@dataclass
class MaintenanceAction:
    """Dataclass representing a single maintenance action or recommendation."""
    issue_identified: str
    recommendation: str
    steps: List[str]
    required_tools: List[str]
    required_parts: List[str]


@dataclass
class FinalRecommendation:
    """Dataclass representing the final aggregated recommendation report."""
    alert_context: str
    actions: List[MaintenanceAction]
    confidence_score: float


class RecommendationEngine:
    """
    Analyzes retrieved document chunks to generate prescriptive maintenance guidance.
    """

    def __init__(self, llm_client: Optional[Any] = None):
        """
        Initializes the RecommendationEngine.

        Args:
            llm_client: Optional LLM client (e.g., LangChain LLM or OpenAI client)
                        used to parse chunks and generate structured recommendations.
                        If None, falls back to a deterministic heuristic/simulation.
        """
        self.llm_client = llm_client
        logger.info("RecommendationEngine initialized.")

    def analyze_chunks(
        self, 
        retrieved_chunks: List[str], 
        alert_context: str = "General Maintenance Inquiry"
    ) -> FinalRecommendation:
        """
        Analyzes retrieved chunks and generates a structured maintenance recommendation.

        Args:
            retrieved_chunks (List[str]): The document chunks retrieved by the search engine.
            alert_context (str): The context or IoT alert triggering this analysis.

        Returns:
            FinalRecommendation: Structured object containing steps, tools, and parts.
            
        Raises:
            ValueError: If the retrieved_chunks list is empty.
        """
        # Input validation and sanitization
        if not retrieved_chunks or not isinstance(retrieved_chunks, list):
            logger.error("Retrieved chunks must be a non-empty list.")
            raise ValueError("Retrieved chunks cannot be empty or malformed.")
            
        # Clean chunks (filter out empty or whitespace-only chunks)
        valid_chunks = [str(c).strip() for c in retrieved_chunks if c and str(c).strip()]
        if not valid_chunks:
            logger.error("All provided chunks were empty or comprised only of whitespace.")
            raise ValueError("No valid text found in retrieved chunks.")
            
        logger.info(f"Analyzing {len(valid_chunks)} valid chunks for context: '{alert_context}'")

        try:
            # If an LLM client is provided, attempt to generate using the dedicated private method.
            if self.llm_client:
                logger.debug("LLM client detected. Delegating to LLM integration.")
                try:
                    return self._generate_with_llm(valid_chunks, alert_context)
                except NotImplementedError:
                    logger.warning("LLM integration not fully implemented. Falling back to heuristic analysis.")
                except Exception as e:
                    logger.error(f"LLM generation failed: {e}. Falling back to heuristic analysis.")

            # Fallback heuristic / Simulated logic based on the text chunks
            return self._heuristic_analysis(valid_chunks, alert_context)

        except ValueError as ve:
            # Bubble up validation errors immediately
            raise ve
        except Exception as e:
            logger.error(f"Failed to analyze chunks: {e}")
            raise RuntimeError(f"Error during recommendation generation: {str(e)}") from e

    def _generate_with_llm(self, chunks: List[str], alert_context: str) -> FinalRecommendation:
        """
        Private helper method for future LLM integration.
        Designed to interface seamlessly with LangChain or native LLM APIs 
        to extract tools, parts, and steps into a structured FinalRecommendation.
        
        Args:
            chunks (List[str]): Validated text chunks.
            alert_context (str): The maintenance alert context.
            
        Returns:
            FinalRecommendation: Structured recommendation output from the LLM.
            
        Raises:
            NotImplementedError: Currently a placeholder signaling the need for heuristic fallback.
        """
        # TODO: Implement LangChain structured output parser or native LLM tool calling here.
        # Example:
        # prompt = self._build_prompt(chunks, alert_context)
        # response = self.llm_client.invoke(prompt)
        # return self._parse_llm_response(response)
        
        raise NotImplementedError("LLM integration is pending implementation.")

    def _heuristic_analysis(self, chunks: List[str], alert_context: str) -> FinalRecommendation:
        """
        Dynamically extracts tools, parts, and steps from text chunks.
        Used as a robust fallback when an LLM is not provided.
        """
        logger.debug("Running dynamic heuristic analysis on chunks.")
        
        actions = []
        
        # Define dynamic extraction regex patterns and keywords
        tool_keywords = ["wrench", "screwdriver", "multimeter", "pliers", "hammer", "drill"]
        part_keywords = ["seal", "filter", "stator", "o-ring", "valve", "pump", "belt", "cylinder"]
        
        # Process each chunk individually to map actions to specific document contexts
        for i, chunk in enumerate(chunks):
            chunk_lower = chunk.lower()
            
            # Dynamically extract tools
            tools_found = [
                word.title() for word in tool_keywords 
                if re.search(r'\b' + word + r'\b', chunk_lower)
            ]
            
            # Dynamically extract parts
            parts_found = [
                word.title() for word in part_keywords 
                if re.search(r'\b' + word + r'\b', chunk_lower)
            ]
            
            # Dynamically extract actionable steps by splitting sentences
            sentences = re.split(r'(?<=[.!?]) +', chunk)
            steps = [
                s.strip() for s in sentences 
                if s.strip() and len(s.split()) > 3
            ]
            
            # If no clear steps found, provide a generic fallback for this chunk
            if not steps:
                steps = [f"Inspect the component related to document chunk {i+1}."]
                
            # Synthesize the identified issue based on the chunk content
            # Grab the first sentence or first 50 chars as the core issue identifier
            issue = sentences[0] if sentences else f"Issue identified in chunk {i+1}"
            if len(issue) > 100:
                issue = issue[:97] + "..."
                
            action = MaintenanceAction(
                issue_identified=issue,
                recommendation=f"Execute maintenance procedure as defined in document chunk {i+1}.",
                steps=steps,
                required_tools=tools_found if tools_found else ["Standard Tools Required"],
                required_parts=parts_found if parts_found else ["No specific parts explicitly stated"],
            )
            actions.append(action)

        # If we failed to extract any actions, provide a safe fallback
        if not actions:
            actions.append(
                MaintenanceAction(
                    issue_identified="Unspecified maintenance anomaly.",
                    recommendation="Review the source documents manually.",
                    steps=["Power down equipment.", "Consult manufacturer guidelines."],
                    required_tools=["Standard Maintenance Toolkit"],
                    required_parts=["N/A"]
                )
            )

        return FinalRecommendation(
            alert_context=alert_context,
            actions=actions,
            confidence_score=0.75
        )

    def format_recommendation(self, recommendation: FinalRecommendation) -> str:
        """
        Formats the structured recommendation into a human-readable text report.

        Args:
            recommendation (FinalRecommendation): The structured recommendation data.

        Returns:
            str: A formatted string report ready for output.
        """
        logger.info("Formatting final recommendation report.")
        
        report = []
        report.append("="*60)
        report.append(f" PRESCRIPTIVE MAINTENANCE REPORT ")
        report.append("="*60)
        report.append(f"Trigger Alert : {recommendation.alert_context}")
        report.append(f"Confidence    : {recommendation.confidence_score * 100:.1f}%\n")
        
        for i, action in enumerate(recommendation.actions, 1):
            report.append(f"--- Action Item {i} ---")
            report.append(f"Issue          : {action.issue_identified}")
            report.append(f"Recommendation : {action.recommendation}\n")
            
            report.append("Required Tools:")
            for tool in action.required_tools:
                report.append(f"  [ ] {tool}")
            
            report.append("\nRequired Parts:")
            for part in action.required_parts:
                report.append(f"  [ ] {part}")
                
            report.append("\nStep-by-Step Guidance:")
            for step_num, step in enumerate(action.steps, 1):
                report.append(f"  {step_num}. {step}")
            report.append("\n")
            
        report.append("="*60)
        return "\n".join(report)


# ==========================================
# Usage Example
# ==========================================
if __name__ == "__main__":
    # Simulate chunks passed over from search_engine.py
    sample_retrieved_chunks = [
        "If the hydraulic pressure drops below 100 PSI, the main cylinder seal is likely compromised.",
        "To replace the seal, use a 10mm wrench to unbolt the housing.",
        "Ensure the system is depressurized before beginning. You will need a replacement O-Ring Seal."
    ]
    
    # 1. Initialize the engine
    engine = RecommendationEngine()
    
    # 2. Analyze the chunks
    try:
        final_rec = engine.analyze_chunks(
            retrieved_chunks=sample_retrieved_chunks,
            alert_context="Sensor 04: Hydraulic Pressure Low (95 PSI)"
        )
        
        # 3. Format and print the final recommendation
        formatted_report = engine.format_recommendation(final_rec)
        print(formatted_report)
        
    except Exception as e:
        logger.error(f"Execution failed: {e}")
