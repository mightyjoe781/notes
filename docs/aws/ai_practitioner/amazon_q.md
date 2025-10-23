# Amazon Q

## Amazon Q Business

- Fully managed Gen-AI assistant for your employees
- Based on your company's knowledge and data
- Built on Amazon Bedrock (but you can't use underlying FM)
- Data Connectors (fully managed RAG) - connecting over 40+ popular enterprise data sources
- Plugins - allows you to interact with 3rd party services
![](assets/Pasted%20image%2020251021201421.png)
### IAM Identity Center

- Users can be authenticated through IAM Identity Center
- Users receive responses generated only from the documents they have access to
- IAM Identity Center can be configured with external Identity Providers
    - IdP: Google Login, Microsoft Active Directory…
![](assets/Pasted%20image%2020251021201510.png)
### Admin Controls

- Controls and customize responses to your organizational needs
- Admin controls == Guardrails
- Block specific words or topics
- Respond only with internal information (vs using external knowledge)
- Global controls & topic-level controls (more granular rules)
- Create Gen AI-powered apps without coding by using natural language
- Leverages your company’s internal data, with possibilities of using Plugins

## Amazon Q Developer

- Answer questions about the AWS documentation and AWS service selection
- Answer questions about resources in your AWS account
- Suggest CLI Commands
- Helps to do bill analysis, resolve errors, troubleshooting
- Al code companion to help you code new applications (similar to GitHub Copilot)
- Supports many languages: Java, JavaScript, Python, TypeScript, C#... Real-time code suggestions and security scans
- Software agent to implement features, generate documentation, bootstrapping new projects

### IDE Extensions

- Integrates with IDE (Integrated Development Environment) to help with your software development needs

## Q in Other AWS Services

### Amazon Q for Quicksight

- Amazon QuickSight is used to visualize your data and create dashboards about them
- Amazon Q understands natural language that you use to ask questions about your data
- Create executive summaries of your data
- Ask and answer questions of data
- Generate and edit visuals for your dashboards

### Amazon Q for EC2

- EC2 instances are the virtual servers you can start in AWS
- Amazon Q for EC2 provides guidance and suggestions for EC2 instance types that are best suited to your new workload
- Can provide requirements using natural language to get even more suggestions or ask for advice by providing other workload requirements

### Amazon Q for Glue

- AWS Glue is an "ETL" (Extract Transform and Load) service used to move data across places 
- Amazon Q for Glue can help with...
- Chat:
    - Answer general questions about Glue
    - Provide links to the documentation
- Data integration code generation:
    - answer questions about AWS Glue ETL scripts
    - generate new code
- Troubleshoot:
    - understand errors in AWS Glue jobs
    - provide step-by-step instructions, to root cause and resolve your issues.

### Amazon Q for AWS Chatbot

- AWS Chatbot is a way for you to deploy an AWS Chatbot in a Slack or Microsoft Teams channel that knows about your AWS account
- Troubleshoot issues, receive notifications for alarms, security findings, billing alerts, create support request
- You can access Amazon Q directly in AWS Chatbot to accelerate understanding of the AWS services, troubleshoot issues, and identify remediation paths
### PartyRock

- GenAl app-building playground (powered by Amazon Bedrock)
- Allows you to experiment creating GenAl apps with various EMs (no coding or AWS account required)
- Ul is similar to Amazon Q Apps (with less setup and no AWS account required)