---
layout: default
title: Projects
permalink: /projects/
---

<h2>Projects & Code</h2>

<div class="projects-grid">
  <div class="project-card">
    <h3>Computer Vision for Medical Imaging</h3>
    <p>As part of a European Union Horizon 2020 grant, I led a team that built a deep learning model for automated classification of CT scan contrast phases, enabling our collaborators at Oxford to curate data for digital contrast.</p>
    <p><strong>Performance:</strong> 95%+ accuracy</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">Deep Learning</span>
      <span class="tag">Medical Imaging</span>
      <span class="tag">PyTorch</span>
    </div>
    <div class="project-links">
      <span style="color: var(--text-secondary); font-style: italic;">EU Horizon 2020 collaboration</span>
    </div>
  </div>

  <div class="project-card">
    <h3>Lilly TuneLab</h3>
    <p>I worked on TuneLab, an AI/ML platform launched by Eli Lilly that gives biotech companies access to drug discovery models trained on Lilly's proprietary data. The platform uses Rhino's federated computing platform so smaller biotech firms can leverage Lilly's AI capabilities while protecting each party's sensitive data &mdash; one of the largest active deployments of federated computing across enterprises.</p>
    <p><strong>Impact:</strong> Enabled pharmaceutical partnerships while maintaining strict data privacy.</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">Federated Learning</span>
      <span class="tag">FHIR</span>
      <span class="tag">Docker</span>
    </div>
    <div class="project-links">
      <span style="color: var(--text-secondary); font-style: italic;">Proprietary - Rhino Federated Computing</span>
    </div>
  </div>

  <div class="project-card">
    <h3>Data Harmonization Engine (RhinoDHE)</h3>
    <p>Led the development of RhinoDHE, which uses GenAI to streamline data harmonization with human-in-the-loop validation while ensuring data stays behind the data custodians' firewalls.</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">OMOP</span>
      <span class="tag">FHIR</span>
      <span class="tag">ETL</span>
    </div>
    <div class="project-links">
      <span style="color: var(--text-secondary); font-style: italic;">Proprietary - Rhino Federated Computing</span>
    </div>
  </div>

  <div class="project-card">
    <h3>RAG System for Healthcare Benefits</h3>
    <p>Built a chatbot for Rightway's care coordination staff to query insurance coverage for specific procedures or medications, requiring parsing of Explanation of Benefits documents from multiple health insurers.</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">OpenAI API</span>
      <span class="tag">RAG</span>
    </div>
    <div class="project-links">
      <span style="color: var(--text-secondary); font-style: italic;">Proprietary - Rightway Healthcare</span>
    </div>
  </div>

  <div class="project-card">
    <h3>Visual Analytics for Patient-Generated Data</h3>
    <p>Interactive visualization system for pattern recognition in patient-generated health data, featuring automated anomaly detection and temporal pattern discovery.</p>
    <p><strong>Published:</strong> JAMIA</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">D3.js</span>
      <span class="tag">Flask</span>
      <span class="tag">ML</span>
    </div>
    <div class="project-links">
      <a href="{{ '/pdfs/jamia_2018.pdf' | relative_url }}">Read the paper (PDF)</a>
    </div>
  </div>

  <div class="project-card">
    <h3>Clinical NLP for HIV Risk</h3>
    <p>NLP pipeline to extract HIV risk factors from unstructured clinical notes, including named entity recognition, relation extraction, and risk scoring.</p>
    <p><strong>Published:</strong> JAIDS</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">NLP</span>
      <span class="tag">scikit-learn</span>
    </div>
    <div class="project-links">
      <a href="{{ '/pdfs/jaids_2018.pdf' | relative_url }}">Read the paper (PDF)</a>
    </div>
  </div>

  <div class="project-card">
    <h3>NLP System for Social Determinants of Health</h3>
    <p>Semi-supervised learning system for extracting social and behavioral determinants from clinical notes, including a gold-standard annotated corpus for training.</p>
    <p><strong>Published:</strong> AMIA 2018</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">NLP</span>
      <span class="tag">Semi-supervised Learning</span>
    </div>
    <div class="project-links">
      <a href="{{ '/pdfs/amia_2019.pdf' | relative_url }}">Read the paper (PDF)</a>
    </div>
  </div>

  <div class="project-card">
    <h3>OMOP Analysis Utilities</h3>
    <p>Python utilities for working with OMOP Common Data Model databases, including cohort builders, data quality checks, and common analysis patterns.</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">SQL</span>
      <span class="tag">OMOP</span>
      <span class="tag">Pandas</span>
    </div>
  </div>

  <div class="project-card">
    <h3>Population Health Dashboards</h3>
    <p>Interactive dashboards for population health management and quality reporting, with real-time visualization of care gaps, outcomes metrics, and health disparities.</p>
    <div class="project-tags">
      <span class="tag">Python</span>
      <span class="tag">Plotly</span>
      <span class="tag">Dash</span>
      <span class="tag">PostgreSQL</span>
    </div>
  </div>
</div>
