def generate_outreach(candidate: dict, job: dict):
    message = f"""
Hi {candidate['name']},

We are hiring for a {job['title']} role.
Your experience in {', '.join(candidate['skills'])} looks relevant.

Interested in a quick discussion?

Regards,
AI Recruiter
"""
    return {"message": message.strip()}
