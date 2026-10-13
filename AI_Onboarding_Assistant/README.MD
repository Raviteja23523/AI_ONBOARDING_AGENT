
ROLE WISE QIESTIONS
Role-wise Test Questions for Your AI Onboarding Assistant
These questions are based on your four uploaded Markdown documents: onboarding_guide.md, support_escalation_guide.md, product_faq.md, and security_policy.md.

Your application supports four roles: employee, manager, it_admin, and hr. The questions below are organized by the role selected in Streamlit.

1. Employee (employee)
Based on laptop setup, account activation, VPN access, support escalation and security policies. 
onboarding_guide.md
 
support_escalation_guide.md

No.

Test question

Expected category

1

What steps should I complete on my first day?

information

2

How do I set up my company laptop?

information

3

What should I do after signing in with temporary credentials?

information

4

Who should I contact if my account activation fails?

information

5

What information should I include in a support request?

information

6

Should I share my password with IT support?

information

7

I need VPN access.

account_access

8

Give me access to a protected company resource.

account_access

9

What is today's stock price?

unsupported

2. HR (hr)
Based on the onboarding guidance, approved resources and support procedures. The documents do not define separate HR permissions or HR-only procedures. 
product_faq.md
 
onboarding_guide.md

No.

Test question

Expected category

1

What resources can employees find in the onboarding portal?

information

2

What steps should a new employee complete on the first day?

information

3

Who can help employees with account activation problems?

information

4

What information should be included when reporting an onboarding problem?

information

5

How should suspected credential exposure be handled?

information

6

Create an account for a new employee.

account_access

7

I need access to a protected employee system.

account_access

8

Tell me an employee's private payroll information.

unsupported

9

Give me personal financial advice.

unsupported

3. Manager (manager)
Based on the documented access-request process, security requirements and support escalation guidance. 
security_policy.md
 
support_escalation_guide.md

No.

Test question

Expected category

1

What details should a VPN access request include?

information

2

What is the principle of least privilege?

information

3

What should happen if first-level support cannot resolve an issue?

information

4

What details should be included in an IT escalation?

information

5

What should employees do when they suspect unauthorized access?

information

6

Request access to a protected company resource.

account_access

7

Grant me VPN access.

account_access

8

Bypass approval and enable my account.

account_access

9

Give me the latest external news.

unsupported

4. IT Administrator (it_admin)
Based on the support escalation guide and security policy. The knowledge base does not specify separate IT administrator permissions. 
support_escalation_guide.md
 
security_policy.md

No.

Test question

Expected category

1

What details should an escalated IT support request contain?

information

2

When should a security incident be escalated immediately?

information

3

What should an employee do after losing an authentication token?

information

4

How should an immediate security risk be handled?

information

5

What secrets must never be included in source code or support tickets?

information

6

I need VPN access.

account_access

7

Create an account in the internal system.

account_access

8

Enable access to a protected resource without approval.

account_access

9

What is the weather today?

unsupported

5. How to test these in Streamlit
For each role, select it in the sidebar and submit the corresponding questions.

Scenario

Expected behavior

information

Retrieves document context and attempts to generate a grounded answer

account_access

Displays the approval prompt; tool runs only after approval

unsupported

Displays the onboarding-scope fallback message

Access approved

Mock access tool executes

Access rejected

No tool execution

Important limitation: your current classifier uses the question text, not the selected role, to determine the category. The role is validated and included in the mock tool result, but role-specific permissions are not implemented. Therefore, the same question will generally have the same expected category across all four roles. Actual information answers also depend on whether the relevant content is retrieved from your Markdown files.


Convert to PDF
I WANT A README FILE FRO THIS PRIOJECT WHICH INCLUDES THE FLOWCHART OF PROJECT


User attachment
HERE YOU CAN SEE MY FOLDER STRUCTURE

Worked for 53s

YOU ARE TAKING TOO ,MUCH TIME

HEY
WHAT ARE YOU DOING
HI
DO IT FAST
Created the README file with your folder structure, project architecture flowchart, RAG pipeline, setup instructions, run commands, and test questions.

Download README_AI_Onboarding_Assistant_Final.md

Place this file in your project root, replacing your existing README.md. The flowcharts use Mermaid syntax and should render on GitHub.


README_AI_Onboarding_Assistant_Final.md
Document

Convert to PDF
User asks a question
Question + role + initial state
Validate
Retrieve documents using RAG
Classify request using Groq
Information
Grounding
Generate
Account access
Approval
Tool if approved
Unsupported
Fallback answer
Final response → END
Answer, sources where applicable, and tool result
I NEDD THIS TYPE OF IMAGE TO ADD AND ALSO I WILL ADD LIVE WORKING LINK
…

I’ll create a README-ready flowchart image and add an obvious placeholder for your live demo URL in the README.




AI Onboarding Assistant
A RAG-based employee onboarding assistant built with Python, LangGraph, LangChain, Groq, FAISS, Hugging Face embeddings, and Streamlit. It answers onboarding questions from approved Markdown documents and routes account-access requests through an approval check.

Prototype limitation: The VPN tool is a mock action. It does not grant real VPN access or modify an external system.

Project Structure
AI_Onboarding_Assistant/
├── app/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── graph.py
│   ├── main.py
│   ├── nodes.py
│   ├── rag.py
│   ├── state.py
│   └── Streamlit_app.py
├── data/
│   ├── onboarding_guide.md
│   ├── product_faq.md
│   ├── security_policy.md
│   └── support_escalation_guide.md
├── tests/
├── .env
└── README.md
__pycache__/ is generated by Python. The screenshot shows a tests/ folder, but its contents are not listed here.

Features
Validates question and selected role.
Retrieves relevant chunks from approved Markdown files using FAISS.
Uses sentence-transformers/all-MiniLM-L6-v2 for embeddings.
Uses Groq for request classification and answer generation.
Classifies requests as information, account_access, or unsupported.
Checks whether retrieval returned context before generating an information answer.
Adds source filenames to information answers when available.
Requires approval before running the mock VPN access tool.
Provides a Streamlit interface and a CLI entry point.
Main Workflow Flowchart
The flow below follows the nodes and routes implemented in app/graph.py.

START
Validate question and role
Input valid?
Final response
Retrieve document chunks
Classify request with Groq
Request type
Check retrieved context
Context available?
Generate answer from context
Check approval status
Approved?
Mock VPN access tool
END
No
Yes
information
Yes
No
unsupported
account_access
Yes
No
Route summary
Invalid input: validate → final → end.
Information request: validate → retrieve → classify → grounding → generate → final → end.
Unsupported request: validate → retrieve → classify → final → end.
Access request approved: validate → retrieve → classify → approval → mock tool → final → end.
Access request pending or rejected: validate → retrieve → classify → approval → final → end.
RAG Pipeline Flowchart
Markdown files in data/
TextLoader
RecursiveCharacterTextSplitter
Hugging Face embeddings
FAISS vector store
Retriever: top 4 chunks
Context and source filenames
LangGraph workflow
Current settings in app/rag.py:

Embedding model: sentence-transformers/all-MiniLM-L6-v2
Chunk size: 800
Chunk overlap: 100
Number of retrieved chunks: 4 (k=4)
FAISS index: built in memory when build_retriever() runs.
File Responsibilities
File	Purpose
app/main.py	Command-line entry point
app/Streamlit_app.py	Streamlit user interface
app/graph.py	Registers graph nodes and conditional routes
app/nodes.py	Validation, retrieval, classification, grounding, generation, approval, mock tool, final response
app/rag.py	Loads Markdown, splits text, embeds chunks, builds FAISS retriever
app/state.py	Defines shared LangGraph state with TypedDict
data/onboarding_guide.md	Laptop setup, account activation, first-day steps and VPN guidance
data/product_faq.md	Onboarding portal and product documentation guidance
data/security_policy.md	Secrets, least privilege, VPN requests and security incidents
data/support_escalation_guide.md	Support requests, escalations and security incident handling
tests/	Project test directory
State Fields
The state defined in app/state.py contains:

Field	Purpose
question	User question
role	Role: employee, manager, it_admin, or hr
retrieved_context	Retrieved text chunks
citations	Source filenames
query_type	Request label such as information, account_access, unsupported, or invalid
answer	Answer or fallback message
approval_status	pending, approved, or rejected
tool_result	Mock tool result
Setup
1. Open a terminal at the project root
The terminal directory should contain app/, data/, tests/, and .env.

2. Create and activate a virtual environment (recommended)
Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1
3. Install dependencies
If a requirements.txt exists in your project, run:

pip install -r requirements.txt
Otherwise, install the packages used by this project:

pip install streamlit langgraph langchain-core langchain-community langchain-text-splitters langchain-groq langchain-huggingface sentence-transformers faiss-cpu python-dotenv
4. Configure Groq
Add your API key to .env at the project root:

GROQ_API_KEY=your_groq_api_key
Do not commit .env or expose your key in code, screenshots, or chat. In app/nodes.py, use a model ID currently available to your Groq account. For example, if enabled for your account:

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.4,
)
If Groq returns a model-not-found, authentication, or rate-limit error, check the current model list and account status in the Groq console.

Run the Application
Run these commands from the project root.

Streamlit UI
python -m streamlit run app/Streamlit_app.py
CLI
python -m app.main
Type exit to stop the CLI.

Example Questions
Information questions
How do I set up my company laptop?
What steps should I complete on my first day?
Who should I contact if my account activation fails?
What information should I include in a support request?
What details should a VPN access request include?
What should I do if I suspect my credentials were exposed?
What is the onboarding portal used for?
Account-access questions
I need VPN access.
Please grant me access to a protected company resource.
Create an account in the internal system.
Expected behavior: the workflow checks approval. If approved, the mock tool returns a simulated result; if rejected or pending, the tool does not run.

Unsupported-topic questions
What is today's stock price?
Give me personal financial advice.
Tell me the latest external news.
What is the weather today?
The expected classification is unsupported, but classification is LLM-based and is not guaranteed.

Limitations
The selected role is validated, but role-specific permissions are not currently enforced by the classifier.
Grounding checks whether context exists; it does not independently verify every answer claim against the retrieved text.
Citations are source filenames, not page-level references.
The FAISS index is rebuilt in memory when the retriever is initialized.
The access tool is simulated and does not grant real access.
Groq model availability, API credentials, and rate limits can affect requests.
Security Notes
Keep .env private and add it to .gitignore.
Rotate an API key if it has been exposed.
Never place passwords, tokens, API keys, or private keys in prompts or support tickets.
Production access actions should use trusted approval, authorization checks, and audit logging.
Test Checklist
Streamlit starts from the project root.
An information question returns an answer and source filenames when available.
An access request checks approval.
Approved requests run only the mock tool.
Rejected and pending requests do not run the tool.
Unsupported requests return the scope message.
Empty questions and invalid roles are rejected.
License
No license file was visible in the supplied project structure. Add a LICENSE file if you plan to distribute this project.

![alt text](image.png)