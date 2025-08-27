from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import streamlit as st

st.set_page_config(layout="wide")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

model = ChatOpenAI(model=st.session_state["openai_model"],
                   api_key=st.secrets["OPENAI_API_KEY"]
                  )

ce = st.empty()

ce_cols = [col for col in  ce.columns(2)]


agenda_str = """
SMART Goal Description
Specific:
A SMART goal should clearly define what needs to be achieved, who is involved, and what actions are required. 
Measurable:
The goal should include metrics or criteria that can be used to track progress and determine if it has been achieved. 
Achievable:
Goals should be realistic and attainable, considering available resources and capabilities. 
Relevant:
The goal should align with overall objectives and contribute to the larger purpose. 
Time-bound:
A SMART goal has a defined deadline or timeframe for completion, creating a sense of urgency and accountability. 
"""

script_str = """
Peter (E-commerce Manager):
Thanks for joining, both of you. 
We’ve been coasting at roughly the same revenue for three months, so it’s time to push harder. 
I want today’s meeting to result in a clear sales growth target we can actually measure. 
Our traffic is steady, but the conversion rate could be better, and I think we need a time-bound target to create urgency. 
It also has to align with our long-term growth strategy. 
So, Alex, from a marketing perspective, what’s a realistic yet challenging sales boost we can aim for?

Alex (Marketing Manager):
Based on our past campaigns, I’d suggest aiming for a 15% increase in sales over the next six months. 
That’s ambitious enough to push us, but still attainable. 
I believe social media advertising could be the main driver here — we’ve had good engagement before, but we haven’t done a fully targeted ad series yet. 
If we invest in precise audience targeting, plus retargeting ads, we could significantly improve conversions. 
I’d also budget for A/B testing of ad creatives so we can optimize mid-campaign. 
But for these ads to truly work, our product pages need to be stronger, and that’s where Greg’s work will be key.

Greg (Content/SEO Specialist):
Absolutely. Even the best ads won’t convert if the landing pages aren’t compelling. 
Right now, some of our product descriptions are too generic and lack strong keywords. 
I can do a full audit in the first two weeks, then rewrite the top 50 best-selling product pages with better SEO and more persuasive copy. 
This should improve both organic traffic and ad conversions. 
I’ll make sure pages have high-quality images, scannable bullet points, and consistent formatting. 
That way, when Alex’s ads bring visitors in, the page itself will do the selling.

Peter
Good. So we’re combining two tactics — a targeted ad campaign and optimized product descriptions — toward one clear sales goal. 
Let’s check if it’s SMART. 
Specific? Yes, we know exactly what we’re doing and why. 
Measurable? Yes, we can track the 15% change. 
Achievable? Based on your input, yes. 
Relevant? Definitely, because it supports our revenue growth plan. 
Time-bound? Six months, so that’s covered.

Alex:
Agreed. I’ll draft the ad strategy this week and share a campaign calendar. 
We should meet bi-weekly to review performance and adjust targeting. 
I’ll coordinate with Greg so the ad copy matches the updated product pages. 
I’ll also prepare seasonal campaign ideas to catch timely interest, and have a contingency budget ready if we see underperformance by month three.

Greg:
I’ll prioritize rewriting the highest-traffic product pages first so we see results sooner. 
I’ll integrate some storytelling elements to make the copy more engaging, choose keywords based on search trends and competitor analysis, 
and use SEO scoring tools before publishing. 
After updates go live, I’ll track changes in organic traffic and conversion rate so we can fine-tune both ads and product presentation mid-campaign.

Peter:
Excellent. 
I’ll document the final SMART goal as: 
“Increase online store sales by 15% in the next 6 months by launching a targeted social media ad campaign and optimizing all product descriptions.”.
 I’ll circulate it with milestones so everyone stays accountable. 
 This will be our main growth initiative for the next two quarters. Let’s make it happen.
"""

script = ce_cols[0].text_area("Input Script", value=script_str,height=300)
agenda = ce_cols[1].text_area("Input Agenda", value=agenda_str,height=300)

#template = """Script: {script}. """
#template += """ Given the agenda {agenda}, analyze which items of the agenda have been discussed. 
#Summarize the dialog script and output results in the form of JSON. The first part (meeting_summary) of output should contain 
#agenda item with summary for each item. The second part (participation) of the output should itemize each participant and 
#for each participant each agenda item should be marked whether a given participant discussed the agenda item. 
#"""

template = """
Given the following meeting agenda and script, please provide a detailed analysis.

## Agenda
{agenda}

## Meeting Script
{script}

## Analysis Instructions
Analyze the meeting script against the agenda items and present your findings in two parts:

1.  **Agenda Coverage:**
    * List each agenda item.
    * For each item, state whether it was discussed.
    * If discussed, quote the specific lines or dialogue from the script that correspond to that item. If not discussed, state that.
    * Example: "Project Zeus Kick-off: Discussed. Relevant script: 'John: "Good morning, everyone. Let's start with our agenda. First, Project Zeus...'"

2.  **Participant Contributions:**
    * For each participant (e.g., John, Jane, Mike), list the agenda items they contributed to.
    * Briefly describe the nature of their contribution (e.g., initiating the topic, providing an update, raising a concern).
    * Example: "John: Contributed to Project Zeus Kick-off (initiated discussion) and Q3 Budget Review (suggested follow-up)."
"""


prompt_template = ChatPromptTemplate.from_template(template)

if st.button("Process Script"):
    prompt = prompt_template.invoke({"script":script,
                                     "agenda":agenda})
    result = model.invoke(prompt)
    response = result.content
    st.write(response)
#else:
#    st.write("Goodbye")