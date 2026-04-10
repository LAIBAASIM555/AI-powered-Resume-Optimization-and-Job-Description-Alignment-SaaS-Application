"""
Dataset Generator for AI Resume Optimizer
Generates 1000+ realistic resume-job matching records for academic/demo purposes.
Run: python generate_dataset.py
"""
import csv
import random
import os

random.seed(42)

# ──────────────── DATA POOLS ────────────────────────────────────────────────

first_names = [
    "Ahmed","Sara","Bilal","Ayesha","Usman","Fatima","Hamza","Zainab","Ali","Mariam",
    "Kamran","Sana","Tariq","Nadia","Imran","Rabia","Omar","Hira","Waqas","Amna",
    "Junaid","Asma","Shahid","Lubna","Rizwan","Sofia","Faisal","Nosheen","Irfan","Madiha",
    "Zaid","Iqra","Babar","Huma","Naeem","Sobia","Adnan","Aroha","Waseem","Saima",
    "Shahroz","Mehwish","Usman","Nadia","Aamir","Zara","Tariq","Aisha","Faizan","Laiba",
    "Hassan","Maryam","Jawad","Sidra","Salman","Rimsha","Adeel","Komal","Fahad","Nimra",
    "Danial","Aliya","Zahid","Kiran","Talha","Mehak","Saad","Amara","Shoaib","Qurat",
    "Abdullah","Tayyba","Yasir","Aneesa","Mujtaba","Zoya","Sohail","Hina","Asad","Bushra",
    "Nabeel","Rukhsana","Shahzad","Fozia","Waheed","Samia","Nasir","Amber","Farhan","Ghazala",
    "Majid","Rubina","Karim","Farah","Rehan","Anam","Ahsan","Nazia","Raza","Sahar",
    "James","Emily","Michael","Jessica","David","Sarah","Robert","Lisa","William","Karen",
    "Richard","Nancy","Joseph","Margaret","Thomas","Betty","Charles","Sandra","Christopher","Dorothy",
    "Daniel","Ashley","Matthew","Kimberly","Anthony","Emily","Mark","Donna","Donald","Carol",
    "Steven","Ruth","Paul","Sharon","Andrew","Michelle","Kenneth","Laura","George","Susan",
    "Noah","Olivia","Liam","Emma","Ethan","Ava","Lucas","Isabella","Mason","Mia",
    "Logan","Amelia","Jackson","Harper","Sebastian","Evelyn","Aiden","Abigail","Owen","Ella"
]

last_names = [
    "Khan","Ali","Mahmood","Siddiqui","Tariq","Noor","Iqbal","Raza","Hassan","Shah",
    "Baig","Malik","Javed","Qureshi","Hussain","Aslam","Farooq","Butt","Anwar","Khalid",
    "Akhtar","Saleem","Ahmed","Zafar","Rashid","Niazi","Chaudhry","Rana","Shahzad","Ansar",
    "Mehmood","Pervez","Islam","Ashfaq","Cheema","Farhan","Smith","Johnson","Williams","Brown",
    "Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson",
    "Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White",
    "Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King",
    "Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker"
]

job_titles_by_field = {
    "Software Engineering": [
        ("Junior Python Developer","Python;Flask;MySQL;Git;HTML;CSS","FastAPI;PostgreSQL;Docker;Redis","Learn FastAPI and PostgreSQL;Containerize apps with Docker","$45,000 - $70,000",1,3),
        ("Python Backend Developer","Python;FastAPI;PostgreSQL;Git;Docker;SQLAlchemy","Kubernetes;Celery;Redis;Microservices","Learn Kubernetes for orchestration;Add Celery for async tasks","$65,000 - $100,000",2,5),
        ("Senior FastAPI Engineer","Python;FastAPI;PostgreSQL;Redis;Docker;Kubernetes;Microservices;JWT","GraphQL;gRPC;Event Sourcing;CQRS","Study GraphQL federation;Learn gRPC for internal services","$100,000 - $145,000",5,9),
        ("Java Spring Boot Developer","Java;Spring Boot;MySQL;REST API;Maven;JUnit","Kafka;Redis;Microservices;Docker","Learn Apache Kafka for messaging;Add Docker to your workflow","$70,000 - $110,000",3,6),
        ("C# .NET Developer","C#;.NET Core;SQL Server;REST API;Git;Entity Framework","Azure;Docker;gRPC;MAUI","Get Azure certified;Learn gRPC for internal APIs","$70,000 - $115,000",2,6),
        ("Go Backend Engineer","Go;REST API;PostgreSQL;Docker;Redis","gRPC;Kubernetes;Prometheus;Service Mesh","Learn gRPC with Go;Study Istio service mesh","$90,000 - $135,000",4,7),
        ("Rust Systems Developer","Rust;Systems Programming;WebAssembly;Async_Rust;CLI","Embedded Rust;LLVM;Formal Verification","Explore embedded Rust;Study formal verification with Prusti","$95,000 - $140,000",3,6),
        ("Node.js Backend Developer","Node.js;Express;MongoDB;JavaScript;TypeScript;JWT","NestJS;GraphQL;Redis;Kafka","Migrate from Express to NestJS;Learn GraphQL","$65,000 - $100,000",2,5),
        ("Full Stack Developer","React;Node.js;MongoDB;TypeScript;Docker;REST API","AWS;Kubernetes;GraphQL;CI/CD","Get AWS certified;Add GraphQL to your API","$75,000 - $120,000",3,7),
        ("Software Architect","System Design;Microservices;Cloud Architecture;REST API;Docker;Kubernetes;SQL;NoSQL","Event-Driven Architecture;CQRS;DDD","Study Domain-Driven Design;Learn CQRS and Event Sourcing","$130,000 - $180,000",8,12),
    ],
    "Data Science": [
        ("Junior Data Scientist","Python;Pandas;NumPy;Matplotlib;Scikit-learn;SQL","TensorFlow;Deep Learning;Feature Engineering;MLflow","Start learning deep learning with TensorFlow;Study feature engineering","$55,000 - $85,000",0,2),
        ("Data Scientist","Python;Scikit-learn;TensorFlow;Pandas;SQL;Matplotlib;Statistics","Spark;MLflow;Dask;Bayesian Methods","Learn Apache Spark for big data;Add MLflow for experiment tracking","$85,000 - $130,000",3,6),
        ("Senior Data Scientist","Python;PyTorch;TensorFlow;Scikit-learn;SQL;Statistics;A/B Testing;MLflow;Spark","Causal Inference;Reinforcement Learning;LLM Fine-tuning","Study causal inference;Explore LLM fine-tuning with LoRA","$110,000 - $155,000",5,9),
        ("ML Research Scientist","PyTorch;Deep Learning;NLP;Computer Vision;Research;Python;JAX","RLHF;Diffusion Models;Distributed Training","Publish research on arXiv;Study diffusion model architecture","$120,000 - $175,000",5,10),
        ("Applied ML Scientist","Python;Scikit-learn;TensorFlow;Experiment Design;Statistics;SQL","AutoML;Feature Stores;Model Monitoring","Learn feature store design;Add model monitoring with Evidently","$100,000 - $145,000",4,8),
        ("Biostatistician","R;Python;SAS;Clinical Trial Data;Biostatistics;SPSS","CDISC Standards;Survival Analysis;Bayesian Clinical Trials","Master CDISC SDTM/ADaM;Study Bayesian adaptive clinical trials","$80,000 - $120,000",3,7),
    ],
    "Data Engineering": [
        ("Junior Data Engineer","Python;SQL;PostgreSQL;Pandas;Git","Airflow;Spark;Kafka;dbt;Data Warehouse","Learn Apache Airflow for scheduling;Set up dbt for data transformation","$60,000 - $90,000",1,3),
        ("Data Engineer","Python;Spark;Airflow;PostgreSQL;Kafka;dbt;Redshift","Delta Lake;Streaming;Flink;Great Expectations","Add Delta Lake for ACID transactions;Learn stream processing with Flink","$90,000 - $130,000",3,6),
        ("Senior Data Engineer","Python;Spark;Kafka;Airflow;dbt;BigQuery;Terraform;Delta Lake","Real-time ML Features;Lakehouse;DuckDB;Reverse ETL","Learn lakehouse architecture;Explore DuckDB for lightweight analytics","$115,000 - $160,000",5,9),
        ("Data Architect","Data Modeling;Snowflake;BigQuery;dbt;Lakehouse;Governance;Metadata","DataMesh;DataContract;Catalog (Amundsen);Cost Optimization","Study Data Mesh principles;Learn data cataloging with Amundsen","$130,000 - $180,000",8,12),
    ],
    "DevOps & Cloud": [
        ("Cloud Engineer","AWS;Terraform;Linux;Docker;Git;CI/CD","Kubernetes;Ansible;Monitoring;Cost Optimization","Get Kubernetes certified (CKA);Study FinOps for cost optimization","$80,000 - $120,000",2,5),
        ("DevOps Engineer","Docker;Kubernetes;CI/CD;Terraform;AWS;Linux;Python;Ansible","Observability (Prometheus/Grafana);GitOps;ArgoCD","Set up Prometheus+Grafana stack;Learn ArgoCD for GitOps","$90,000 - $135,000",3,7),
        ("Senior SRE","Linux;Kubernetes;Python;Prometheus;Grafana;Terraform;AWS;Go;SLO;SLA","Chaos Engineering;eBPF;Tracing (Jaeger)","Implement chaos experiments with LitmusChaos;Learn distributed tracing","$120,000 - $165,000",6,10),
        ("Cloud Architect","AWS;Azure;GCP;Terraform;Kubernetes;Security;Networking;Cost Architecture","Multi-Cloud;Zero Trust;FinOps;Cloud Native","Study Well-Architected Framework for all three clouds;Get FinOps certified","$140,000 - $200,000",8,13),
        ("Platform Engineer","Kubernetes;Terraform;Helm;ArgoCD;Python;Go;Internal Developer Platforms","Backstage;Crossplane;Policy as Code (OPA)","Build internal developer portal with Backstage;Learn Crossplane for infra abstraction","$110,000 - $155,000",5,9),
    ],
    "AI & Machine Learning": [
        ("ML Engineer","Python;TensorFlow;PyTorch;Docker;MLflow;Feature Engineering;SQL","Kubernetes;Ray;Model Serving;Real-time Inference","Learn Ray for distributed training;Set up real-time model serving","$100,000 - $145,000",3,6),
        ("NLP Engineer","Python;spaCy;NLTK;Transformers;BERT;Hugging Face;TensorFlow","LLM Fine-tuning;RLHF;RAG;LangChain","Study RAG architecture;Learn LangChain for LLM application development","$100,000 - $148,000",3,6),
        ("Computer Vision Engineer","Python;OpenCV;PyTorch;YOLO;Image Segmentation;Deep Learning","ONNX;Edge Deployment;3D Point Cloud;Video Analytics","Learn ONNX optimization for edge;Study point cloud algorithms for autonomous vehicles","$103,000 - $150,000",3,7),
        ("LLM Engineer","Python;LangChain;OpenAI API;RAG;Vector Databases;Prompt Engineering;FastAPI","Fine-tuning;RLHF;LlamaIndex;Multi-agent Systems","Study multi-agent LLM orchestration;Learn LlamaIndex for complex RAG","$115,000 - $165,000",2,5),
        ("AI Research Scientist","PyTorch;Deep Learning;Research;Python;Statistics;JAX;LaTeX","RLHF;Diffusion Models;Mechanistic Interpretability;Alignment","Submit papers to NeurIPS/ICML;Study mechanistic interpretability","$125,000 - $185,000",5,12),
    ],
    "Web Development": [
        ("Frontend Developer","React;JavaScript;HTML;CSS;Tailwind CSS;Git","TypeScript;Next.js;Jest;Storybook;Accessibility","Learn TypeScript;Add unit testing with Jest;Study accessibility (WCAG)","$60,000 - $95,000",1,4),
        ("React Developer","React;TypeScript;Redux;REST API;Tailwind CSS;Git;Jest","Next.js;GraphQL;Storybook;React Query","Learn Next.js for SSR/SSG;Add React Query for server state","$75,000 - $110,000",2,5),
        ("Next.js Developer","Next.js;React;TypeScript;Tailwind CSS;Vercel;REST API;Prisma","GraphQL;tRPC;Edge Runtime;Planetscale","Learn tRPC for type-safe APIs;Study Edge Runtime performance","$85,000 - $125,000",3,6),
        ("Vue.js Developer","Vue.js;JavaScript;Tailwind CSS;Pinia;REST API;Git","TypeScript;Nuxt.js;GraphQL;Vite Tests","Learn TypeScript with Vue 3;Migrate to Nuxt.js for SSR","$70,000 - $105,000",2,5),
        ("Angular Developer","Angular;TypeScript;RxJS;Angular Material;REST API;NgRx","Micro-frontend (Module Federation);Unit Testing (Jasmine);NX Monorepo","Study micro-frontend architecture;Set up NX monorepo","$75,000 - $115,000",3,6),
    ],
    "Mobile Development": [
        ("Android Developer","Kotlin;Android SDK;Jetpack Compose;Room;Retrofit;MVVM;Coroutines","Compose Multiplatform;Hilt DI;Firebase;CI/CD","Learn Compose Multiplatform;Integrate Firebase Analytics","$75,000 - $115,000",2,5),
        ("iOS Developer","Swift;UIKit;SwiftUI;Core Data;Combine;MVVM;Xcode","WidgetKit;In-App Purchase;Firebase;Fastlane","Learn WidgetKit development;Automate App Store submission with Fastlane","$80,000 - $125,000",2,6),
        ("React Native Developer","React Native;TypeScript;Expo;Redux;REST API;Firebase","Reanimated 3;Native Modules;New Architecture","Learn Reanimated 3 for animations;Study React Native New Architecture","$70,000 - $108,000",2,5),
        ("Flutter Developer","Flutter;Dart;BLoC;REST API;Firebase;Provider","Riverpod;Platform Channels;Isolates","Migrate from BLoC to Riverpod;Learn platform channel integrations","$72,000 - $110,000",2,5),
        ("Mobile Architect","Swift;Kotlin;React Native;Architecture Patterns;CI/CD;Security;Performance","Compose Multiplatform;Modularization;App Clips","Study large-scale app modularization;Implement app clip experiences","$120,000 - $165,000",6,10),
    ],
    "Cybersecurity": [
        ("Security Analyst","Network Security;SIEM;Firewalls;Linux;Incident Response;Vulnerability Scanning","Threat Intelligence;SOAR;Cloud Security;Zero Trust","Learn SOAR playbook automation;Study cloud security fundamentals","$70,000 - $105,000",1,4),
        ("Penetration Tester","Kali Linux;Metasploit;Burp Suite;OSINT;SQL Injection;Python;Network Hacking","Custom Exploit Dev;Red Team Ops;OSCP Extension;Cloud Pentesting","Develop custom post-exploitation tools;Learn cloud penetration testing","$85,000 - $130,000",2,6),
        ("Cloud Security Engineer","AWS Security;IAM;GuardDuty;WAF;SIEM;Python;Terraform","Zero Trust;CWPP;CSPM;DevSecOps","Implement CSPM with Wiz or Prisma;Study Zero Trust architecture","$100,000 - $145,000",3,7),
        ("SOC Analyst","SIEM (Splunk);Incident Response;Malware Analysis;Network Forensics;Linux","SOAR;Threat Hunting;Reverse Engineering;MITRE ATT&CK","Learn SOAR for automated response;Study MITRE ATT&CK Navigator","$65,000 - $100,000",1,4),
        ("AppSec Engineer","OWASP Top 10;SAST;DAST;Threat Modeling;Python;Security Code Review;Burp Suite","IAST;Supply Chain Security;SBOM;Shift-Left Security","Implement dependency scanning (Snyk);Study SBOM generation","$95,000 - $140,000",4,7),
    ],
    "Data Analytics": [
        ("Data Analyst","SQL;Excel;Tableau;Python;Power BI;Data Visualization","R;Machine Learning;Advanced Statistics;Data Storytelling","Learn R for statistical analysis;Begin ML fundamentals","$55,000 - $85,000",1,3),
        ("Business Intelligence Analyst","SQL;Power BI;Tableau;Excel;DAX;SSAS;ETL","Looker;Snowflake;dbt;Advanced DAX","Learn Looker for modern BI;Study dbt for data transformation","$70,000 - $105,000",3,6),
        ("Marketing Analyst","SQL;Google Analytics;Tableau;A/B Testing;Python;Meta Ads API;Excel","Mixpanel;Amplitude;Attribution Modeling;Marketing Mix Modeling","Learn multi-touch attribution;Study Marketing Mix Modeling","$65,000 - $95,000",2,5),
        ("Financial Analyst","Excel;Financial Modeling;SQL;Power BI;VBA;Bloomberg","Python for Finance;Monte Carlo Simulation;FP&A Automation","Add Python automation to replace VBA;Study Monte Carlo modeling","$70,000 - $105,000",2,6),
        ("Product Analyst","SQL;Amplitude;A/B Testing;Python;Tableau;User Funnel Analysis","Causal Inference;ML for Product;DataOps","Study causal inference for experiment decision making;Add ml-based segmentation","$80,000 - $115,000",3,6),
    ],
    "UI/UX Design": [
        ("UI Designer","Figma;Adobe Photoshop;Wireframing;Prototyping;Design Systems","Motion Design;Framer;Accessibility;Interaction Design","Learn Framer for advanced prototypes;Study WCAG 2.1 accessibility","$55,000 - $85,000",1,3),
        ("UX Designer","Figma;User Research;Usability Testing;Journey Mapping;Wireframing;Prototyping","Quantitative UX Research;DesignOps;LLM UX Patterns","Learn quantitative UX research methods;Study AI/LLM UX design patterns","$70,000 - $105,000",2,5),
        ("Product Designer","Figma;Design Systems;UX Research;Prototyping;Interaction Design;HTML;CSS","Design Tokens;Storybook Integration;Accessibility Audit","Build a Storybook component library from your design system;Learn accessibility auditing","$85,000 - $125,000",3,6),
    ],
    "DevOps & Cloud": [
        ("Kubernetes Engineer","Kubernetes;Docker;Helm;Terraform;Go;Python","Service Mesh (Istio);Cluster API;GitOps;OPA","Deploy Istio for mTLS between services;Study Cluster API for multi-cluster","$100,000 - $145,000",4,7),
        ("AWS Cloud Developer","AWS Lambda;S3;DynamoDB;API Gateway;Python;CDK;CloudFormation","Step Functions;EventBridge;AppSync;Bedrock","Build with AppSync for GraphQL on AWS;Study Bedrock for AI on AWS","$90,000 - $135,000",3,6),
    ],
    "Database Engineering": [
        ("Database Administrator","PostgreSQL;MySQL;Backup;Replication;Performance Tuning;SQL","MongoDB;Redis;Cloud Databases;Partitioning","Learn AWS RDS for cloud;Study horizontal partitioning","$80,000 - $120,000",4,8),
        ("Database Architect","Data Modeling;PostgreSQL;Distributed Systems;Sharding;CQRS;Event Sourcing","NewSQL (CockroachDB);HTAP;Global Distribution","Study CockroachDB for globally distributed databases;Learn HTAP systems","$120,000 - $165,000",7,12),
    ],
    "Product Management": [
        ("Product Manager","Agile;JIRA;Product Roadmap;User Research;Stakeholder Management;PRD Writing","SQL;Data Analysis;A/B Testing;OKRs","Learn SQL for data-driven decisions;Study A/B testing statistical significance","$85,000 - $125,000",3,6),
        ("Senior Product Manager","Agile;OKRs;JIRA;Data Analysis;SQL;Stakeholder Alignment;GTM Strategy;Pricing","AI Product Concepts;Platform Strategy;Network Effects","Deep-dive into platform strategy;Study AI product design principles","$110,000 - $155,000",5,9),
        ("AI Product Manager","AI Concepts;LLMs;Product Roadmap;OKRs;User Research;Agile;Data Analysis","LLM Evaluation;Responsible AI;ML Pipeline Knowledge;RAG","Study LLM evaluation and red-teaming;Learn responsible AI frameworks","$120,000 - $165,000",4,8),
    ],
    "Project Management": [
        ("Project Manager","PMP;JIRA;Risk Management;Stakeholder Mgmt;Budget;MS Project;Agile","Program Management;OKR;Change Management;SAFe","Get SAFe Program Consultant cert;Study change management frameworks","$80,000 - $115,000",3,7),
        ("Scrum Master","Scrum;Kanban;JIRA;Agile Coaching;Sprint Planning;Retrospectives","SAFe Agilist;OKRs;DevOps Collaboration;Conflict Resolution","Complete SAFe Agilist certification;Study DevOps and Dev collaboration","$78,000 - $112,000",3,6),
    ],
    "Business Analysis": [
        ("Business Analyst","Requirements Gathering;User Stories;Process Modeling;SQL;JIRA;Stakeholder Mgmt","BPMN;Data Warehouse;Power BI;API Understanding","Build BPMN 2.0 modeling skills;Learn Power BI for self-service analytics","$70,000 - $105,000",3,6),
        ("Senior Business Analyst","CBAP;Requirements Analysis;Data Analysis;SQL;Power BI;Change Management;BPMN","Advanced Analytics;AI Business Cases;Enterprise Architecture","Study enterprise architecture (TOGAF);Build AI business case skills","$95,000 - $135,000",5,9),
    ],
    "FinTech": [
        ("FinTech Backend Engineer","Python;FastAPI;PostgreSQL;Stripe API;Redis;Celery;Docker","PCI DSS;Open Banking;Real-time Payments;Kafka","Study PCI DSS compliance requirements;Learn Open Banking API standards","$100,000 - $150,000",4,7),
        ("Quantitative Analyst","Python;R;Statistics;Monte Carlo;Financial Modeling;Bloomberg;NumPy","Algorithmic Trading;Derivatives Pricing;Risk Management;HFT","Learn derivatives pricing theory;Study risk management frameworks","$110,000 - $165,000",4,9),
    ],
    "Embedded Systems": [
        ("Embedded Software Engineer","C;C++;RTOS;ARM Cortex;Microcontrollers;Embedded Linux;UART;SPI;I2C","AUTOSAR;CAN Bus;Safety Standards (ISO 26262);OTA Updates","Study AUTOSAR architecture;Get ISO 26262 Functional Safety training","$80,000 - $120,000",3,7),
        ("Senior Embedded Engineer","C;C++;RTOS;ARM Cortex;Embedded Linux;CAN Bus;AUTOSAR;ISO 26262","Machine Learning on Edge;V-Model Process;Hardware Co-design","Learn TensorFlow Lite for edge ML;Study hardware-software co-design","$100,000 - $145,000",6,10),
    ],
    "Blockchain": [
        ("Solidity Developer","Solidity;Hardhat;Foundry;ERC-20;ERC-721;Web3.js;JavaScript","DeFi Protocols;ZK-Rollups;Security Auditing;Formal Verification","Learn smart contract security auditing;Study ZK-Rollup scaling","$85,000 - $135,000",2,5),
        ("Blockchain Architect","Solidity;Blockchain Protocols;Consensus Mechanisms;DeFi;Layer 2;Cryptography","Cross-Chain Bridges;ZK Proofs;Tokenomics Design;Governance","Study ZK proof systems (Groth16/PLONK);Design token governance mechanisms","$120,000 - $175,000",5,9),
    ],
    "Game Development": [
        ("Unity Developer","Unity;C#;Game Physics;3D Modeling;Multiplayer;HLSL Shaders","Unreal Engine;VR/AR;Procedural Generation;Netcode","Learn Unreal Engine 5;Study procedural content generation","$55,000 - $85,000",1,4),
        ("Unreal Engine Developer","Unreal Engine 5;C++;Blueprints;Nanite;Lumen;Game Physics","Real-time Ray Tracing;PCG Framework;MetaHumans","Study PCG framework for procedural levels;Learn MetaHuman Creator","$70,000 - $110,000",2,5),
    ],
}

education_levels = ["High School","Associate","Bachelor","Master","PhD","MBA","Bootcamp"]
certifications_pool = [
    "AWS Solutions Architect","Google Cloud Professional","Azure Expert","CKA Certified",
    "PMP","CISSP","OSCP Certified","CEH","CompTIA Security+","Tableau Desktop Specialist",
    "Google Analytics Certified","Salesforce Administrator","CBAP Certified","SHRM-CP",
    "Scrum Master (CSM)","SAFe Agilist","TensorFlow Developer","AWS Developer Associate",
    "Cisco CCNP","Oracle Java SE Professional","SAP Certified Application Associate",
    "Google UX Design Certificate","HubSpot Content Marketing","Adobe Certified Expert",
    "None","None","None","None","None","None"  # weighted towards None
]
companies = [
    "TechCorp","DataDriven Inc","StartupXYZ","CloudMasters","AI Innovations","WebDev Co",
    "DigitalAgency","RetailCorp","EnterpriseSoft","ProductHouse","SecureNet","DesignStudio",
    "DataSystems Inc","MobileWorks","AppFactory","LanguageAI","CryptoTech","QualityFirst",
    "GameStudio","DocuBase","ReliableOps","BrandBoost","HardwareTech","ConsultingGroup",
    "VisionAI","SprintPro","EnterpriseJava","DataPipeline Inc","ResearchLab","PeopleFirst HR",
    "CrossPlatformApps","ContentHive","NetConnect","CreativeAgency","ERPExperts","SaaSPlatform",
    "DeFiProtocol","PharmaResearch","GrowthEngine","EduTech Corp","SysTech","InsightsCo",
    "CloudNativeCo","AnalyticsFirm","SAPPartner","SecureHack","PayTech","HealthFirst Hospital",
    "AIForward","NexGen Solutions","InnovateX","SmartApps","Finbridge","ByteWave","CloudPeak",
    "DataNexus","OpenStack Inc","PrecisionAI","LogicBridge","MicroScale","Veridian Tech",
    "QuantumLeap","CyberEdge","BluePrint Digital","NovaTech","SynthAI","Aethon Systems",
]
locations = [
    "Remote","New York","San Francisco","Seattle","Austin TX","Chicago","Houston",
    "Boston","Dallas","Los Angeles","Washington DC","Denver","Miami","Atlanta",
    "San Jose","Detroit","Philadelphia","Portland","Phoenix","Minneapolis","Charlotte",
    "London","Toronto","Berlin","Singapore","Dubai","Sydney","Amsterdam","Stockholm",
]

# ──────────────── GENERATION ────────────────────────────────────────────────

def make_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def education_for_field(field):
    if field in ("AI & Machine Learning","Data Science","Research"):
        return random.choice(["Master","Master","PhD","Bachelor","Master"])
    elif field in ("UI/UX Design","Game Development"):
        return random.choice(["Bachelor","Bachelor","Associate","Bootcamp","Master"])
    elif field in ("Product Management","Business Analysis","FinTech"):
        return random.choice(["Bachelor","MBA","Master","Bachelor","MBA"])
    return random.choice(["Bachelor","Bachelor","Master","Bachelor","Associate","Bootcamp"])

rows = []
uid = 1

for field, openings in job_titles_by_field.items():
    needed = max(1, 1000 // len(job_titles_by_field) + 5)
    for _ in range(needed):
        job = random.choice(openings)
        (role, skills_str, missing_str, rec_str, salary_range, min_exp, max_exp) = job

        name = make_name()
        exp = random.randint(min_exp, max_exp + 2)
        edu = education_for_field(field)
        cert = random.choice(certifications_pool)

        # Skills: candidate has most but maybe not all
        all_skills = skills_str.split(";")
        candidate_skills = all_skills if random.random() > 0.3 else all_skills[:-1]

        # Score: correlated with exp and skills coverage
        base_score = 55 + (exp * 4) + random.randint(-8, 10)
        skill_ratio = len(candidate_skills) / max(len(all_skills), 1)
        ats_score = min(99, max(40, int(base_score * skill_ratio)))

        matched = ";".join(candidate_skills)
        missing = missing_str
        rec = rec_str
        company = random.choice(companies)
        location = random.choice(locations)
        demand_options = ["Very High","High","High","Medium","Medium","Low"]
        demand_weights  = [0.30, 0.35, 0.15, 0.10, 0.07, 0.03]
        market_demand = random.choices(demand_options, demand_weights)[0]

        rows.append({
            "resume_id": uid,
            "candidate_name": name,
            "job_title": role,
            "experience_years": exp,
            "education_level": edu,
            "skills": ";".join(candidate_skills),
            "certifications": cert,
            "ats_score": ats_score,
            "job_description_title": role,
            "company": company,
            "location": location,
            "matched_skills": matched,
            "missing_skills": missing,
            "recommendations": rec_str,
            "career_field": field,
            "market_demand": market_demand,
            "salary_range_usd": salary_range,
        })
        uid += 1

# Shuffle for realistic randomness
random.shuffle(rows)
for i, row in enumerate(rows, 1):
    row["resume_id"] = i

# Write out
out_path = os.path.join(os.path.dirname(__file__), "Docs", "dataset.csv")
fieldnames = [
    "resume_id","candidate_name","job_title","experience_years","education_level",
    "skills","certifications","ats_score","job_description_title","company","location",
    "matched_skills","missing_skills","recommendations","career_field","market_demand","salary_range_usd"
]

with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"[OK] Dataset generated: {len(rows)} records -> {out_path}")
