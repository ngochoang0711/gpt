# BusinessAnalysis.io

A minimal web platform to assist Business Analysts.

## Features
- Template library with common BA documents
- Task tracking and automation stubs
- Gamified dashboard showing tasks and progress
- AI assistant placeholder endpoint
- Secure user management with Flask-Login

## Setup
```bash
pip install -r requirements.txt
python run.py
```

Set the `GEMINI_API_KEY` environment variable to enable the AI assistant.

Run tests:
```bash
pytest
```

## Template Library Flow
1. From the **Dashboard** click **"Templates"** to open the library.
2. Browse template cards grouped by category such as Requirements, BA Docs or Stakeholder Maps.
3. Selecting a template opens a preview with options to:
   - **Use in Project**: assign the template to an existing or new project.
   - **Customize**: edit template fields directly in the inline editor.
   - **Download** a PDF or export the content to Notion.

## AI Assistant Flow
1. Access the AI widget from the sidebar or the page toolbar.
2. Enter a prompt like “Write a user story for an eCommerce checkout flow.”
3. The assistant generates a response that you can:
   - Copy to the clipboard.
   - Insert into the current document or template.
   - Regenerate or refine for a better answer.

## Project Management & Workspace Flow
1. From the **Dashboard** choose **"New Project"** and enter the project name, optional client and tags.
2. Select the methodology (Agile, Waterfall or Hybrid) and create the project.
3. You will be redirected to the Project Dashboard which contains tabs for:
   - **Overview** with goals, stakeholders and timeline.
   - **Documents** linking templates or custom files.
   - **Tasks** in Kanban or list view.
   - **Communication Logs** for project discussions.
   - **Analytics** showing progress and effort breakdown.
