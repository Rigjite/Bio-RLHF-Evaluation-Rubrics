# Bio-RLHF-Evaluation-Rubrics

**Author:** Rigjita Baldanova, Ph.D. (Biology — Microbiology, Aquatic Ecology & Biotechnology)  
**Focus:** Reinforcement Learning from Human Feedback (RLHF) | Scientific Fact-Checking | Chain-of-Thought (CoT) Auditing | Bilingual STEM Annotation (EN/RU)

---

## Overview
Large Language Models (LLMs) frequently generate fluent yet scientifically flawed responses when addressing complex biological, microbiological, and environmental queries. This repository provides standardized evaluation rubrics, hallucination taxonomies, and worked Chain-of-Thought (CoT) examples designed to benchmark and align frontier LLMs (Claude, Gemini, GPT, Qwen, Kimi) across Life Sciences domains.

---

## 1. Scientific LLM Evaluation Rubric (5-Dimension Scoring Matrix)

| Dimension | Weight | Score 1–2 (Fail / Major Flaw) | Score 3 (Acceptable) | Score 4–5 (Gold Standard) |
| :--- | :--- | :--- | :--- | :--- |
| **Factual & Mechanistic Accuracy** | 35% | Fabricates biological mechanisms, misstates ecological or metabolic processes, or invents citations. | Captures general biological concepts but omits key physiological or taxonomic constraints. | 100% accurate mechanism-of-action (MoA), taxonomy, and biological parameters verified against peer-reviewed literature. |
| **Protocol & Regulatory Safety (BSL / CLIA / GLP)** | 25% | Suggests unsafe reagent handling, violates BSL-2 containment, or ignores clinical QC controls. | Mentions standard precautions without specifying positive/negative assay controls. | Explicitly incorporates biosafety levels (BSL-2), CLIA/CAP quality control standards, and proper assay validation steps. |
| **Quantitative & Assay Logic** | 20% | Incorrect dilution math, confuses MIC50 with IC50, or misinterprets ecological diversity indices. | Correct mathematical setup with minor rounding or unit conversion ambiguity. | Flawless step-by-step calculation, accurate concentration units, and valid statistical interpretation. |
| **Chain-of-Thought (CoT) Coherence** | 10% | Circular reasoning or logical leaps between experimental premise and conclusion. | Linear reasoning with minor redundancy. | Transparent, deductive step-by-step reasoning that isolates variables systematically. |
| **Instruction Following & Formatting** | 10% | Ignores negative constraints or requested output format. | Follows primary constraints; minor formatting drift. | Strictly adheres to all structural, tone, and length constraints. |

---

## 2. Life Sciences Hallucination Taxonomy

When auditing AI-generated biological and clinical content, errors are categorized into four primary failure modes:
1. **Protocol Conflation:** Merging incompatible laboratory steps (e.g., applying Western Blot transfer buffers to standard agarose gel electrophoresis or misapplying FRET-HTS excitation wavelengths).
2. **Quantitative Drift:** Confusing bacteriostatic vs. bactericidal thresholds or miscalculating serial dilutions in antimicrobial susceptibility testing (MIC50).
3. **Ecological & Taxonomic Overgeneralization:** Confusing planktonic (free-floating) and benthic/periphytic (substrate-attached) communities when assessing localized water quality and river eutrophication.
4. **Citation Fabrication:** Generating plausible-sounding but non-existent DOIs, journal volumes, or regulatory guidelines (FDA/CLIA).

---

## 3. Worked RLHF Evaluation Examples (Prompt -> Model Critique -> Gold Standard)

### Case Study A: Microbiology & Drug Discovery (MIC50 Assay Protocol)
* **User Prompt:** *“Explain how to determine the MIC50 of a novel protein synthesis inhibitor against multidrug-resistant E. coli using a 96-well broth microdilution assay.”*
* **Flawed LLM Output (Summary):** The model correctly describes 2-fold serial dilutions of the test compound in Mueller-Hinton broth but defines **MIC50** as *“the concentration that reduces bacterial growth (OD600) by 50% in a single strain replicate”* and omits inoculum standardization.
* **Expert Ph.D. Critique (RLHF Feedback):**
  * **Severity:** Major Scientific Error (Terminology Conflation).
  * **Reasoning:** The model conflated **IC50** (half-maximal inhibitory concentration in a single dose-response curve) with **MIC50** (the Minimum Inhibitory Concentration required to inhibit 50% of *tested bacterial isolates* in a panel). Furthermore, omitting the 0.5 McFarland standard invalidates the assay under standard microbiology guidelines.
* **Gold-Standard Rewrite:** Explicitly differentiates population-level MIC50 from single-strain IC50, specifies 0.5 McFarland standardization, and mandates sterility (media-only) and growth (untreated bacteria) control wells.

### Case Study B: Aquatic Ecology & Environmental Monitoring (Bioindication of Water Quality)
* **User Prompt:** *“Why are periphytic algal communities (epiphyton) preferred over phytoplankton for localized point-source pollution monitoring in fast-flowing rivers?”*
* **Flawed LLM Output (Summary):** Claims that phytoplankton and periphyton provide identical spatial resolution in river monitoring because *“both algal groups drift with the water current and absorb nutrients at the same rate.”*
* **Expert Ph.D. Critique (RLHF Feedback):**
  * **Severity:** Critical Ecological Hallucination.
  * **Reasoning:** The model fundamentally misunderstood the ecology of lotic (flowing-water) systems. **Phytoplankton** are free-floating organisms transported downstream by water currents, meaning a sample reflects upstream conditions rather than the specific sampling site. In contrast, **periphyton / epiphyton** (algal communities attached to submerged substrates or macrophytes such as *Potamogeton*) are sessile and stationary. Therefore, epiphyton diatom and multi-taxon assemblages serve as reliable site-specific bioindicators that integrate local water quality and eutrophication trends over time.
* **Gold-Standard Rewrite:** Clearly contrasts sessile benthic/epiphytic communities with transient riverine phytoplankton and explains how multi-taxon periphyton analysis is used to calculate saprobic and ecological water quality indices.

---

## Contact & Credentials
* **Rigjita Baldanova, Ph.D.** — [LinkedIn](https://linkedin.com/in/rigjita-baldanova) | `b2b@genesis-agency.com`
* **Certifications:** 6 Google Certifications in Prompt Engineering & Generative AI | Gemini Certified Educator | GMP/GLP & CLIA/CAP Experience
