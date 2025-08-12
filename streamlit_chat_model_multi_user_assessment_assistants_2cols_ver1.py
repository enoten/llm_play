from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import streamlit as st

import matplotlib.pyplot as plt
import numpy as np
from threading import RLock

import json

st.set_page_config(layout="wide")

plt.rcParams['font.size'] = 6

from datetime import datetime


def digalog_analytics(diag_history,
                      speakers):
    topics = list(diag_history[0]["assessment"].keys())
    target_topics = topics[:-1]
    
    speakers_stats = {speaker:{topic:0 for topic in topics} for speaker in speakers}
    
    speaker_counts = {speaker:0 for speaker in speakers}
    speaker_hits = {speaker:0 for speaker in speakers}
        
    for item in diag_history:
        if item["role"] == "user":
            speaker_counts[item["speaker"]] += 1
            for topic in topics:
                speakers_stats[item["speaker"]][topic] += int(item["assessment"][topic])
                if int(item["assessment"][topic]) > 0:
                    if topic in target_topics:
                        speaker_hits[item["speaker"]] += 1
    
    return speakers_stats, speaker_counts, speaker_hits     
        

def get_datetime():
    #return str(datetime.now())
    current_datetime = datetime.now()
    return current_datetime.strftime("%H:%M:%S")


st.title("Chat Bot")

# init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


model = ChatOpenAI(model=st.session_state["openai_model"],
                   api_key=st.secrets["OPENAI_API_KEY"]
                  )

smart_description = """
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

template = smart_description 
template += """ to which item of SMART Goal description this phrase '{topic}' is most relevant to?. 
If the phrase does not match any of the items, please indicate it is off topic.
Provided output in the form of json object with 6 items: 5 items from SMART goals and 1 "Off Topic" item. for 
each item indicate 1 if phrase is relevant for the item, 0 otherwise.
"""

prompt_template = ChatPromptTemplate.from_template(template)

speakers = ("Alex", "Greg", "Peter")

col1, col2 = st.columns(2)


#react to user messages
with col1:
    show_history = st.toggle("Show History JSON")

    speaker = st.selectbox(
        "Speaker?",
        speakers
    )

    #display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["speaker"] + ": " + message["content"])




    prompt = st.chat_input("What is up?")

    if prompt:
        #Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(f"{speaker}: {prompt}")
        #Add  user message to chat history
        st.session_state.messages.append({"role":"user",
                                          "speaker":speaker,
                                          "content": prompt,
                                          "timestamp":get_datetime()
                                        })

           
        prompt = prompt_template.invoke({"topic": prompt})
        result = model.invoke(prompt)
        response = result.content
        #display assistant response in chat message container
        with st.chat_message(name="assistant"):
            st.markdown(response)
        #Add assistant message to chat history
        st.session_state.messages[-1]["assessment"] = json.loads(response)
        st.session_state.messages.append({"role":"assistant",
                                          "speaker":speaker,
                                          "content": response,
                                          "timestamp":get_datetime()                                      
                                        })
    if show_history:  
        st.write(st.session_state.messages)
    #if len(st.session_state.messages)>0:
    #    st.write(digalog_analytics(st.session_state.messages,
    #                               list(speakers)
    #                              )
    #            )
    

with col2:
    _lock = RLock()
    
    if len(st.session_state.messages)>0:
        stats, count, hits = digalog_analytics(st.session_state.messages,
                                               list(speakers)
                                              )

        fig, axs = plt.subplots(3,2, figsize=(6, 3), subplot_kw=dict(aspect="equal"))

        for i in range(len(speakers)):
            ax = axs[i][0]
            topics = list(stats[speakers[i]].keys())
         
            data = list(stats[speakers[i]].values())
#            if count[speakers[i]] > 0: 
#                for i in range(len(data)):
#                    data[i] = data[i]/count[speakers[i]]
            total_freq = sum(data)
            if total_freq > 0:
                data = [dat/total_freq for dat in data]

            ax.bar(topics,data)
            ax.set_title(f"Hits by {speakers[i]}")
            ax.set_ylim(0, 1.25) # Sets the y-axis from 0 to 1
            #ax.set_xticklabels(topics, rotation=45)
            ax.tick_params(axis='x', labelsize=4)

        ax = axs[0][1]
        speaker_labels = list(count.keys())
        data = list(count.values())
        
        ax.pie(data,
               labels=speaker_labels,
               autopct='%1.1f%%',
               textprops={'fontsize': 4}
        )


        #wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40)
        
        #bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        #kw = dict(arrowprops=dict(arrowstyle="-"),
        #          bbox=bbox_props, zorder=0, va="center")

        #for i, p in enumerate(wedges):
        #    ang = (p.theta2 - p.theta1)/2. + p.theta1
        #    y = np.sin(np.deg2rad(ang))
        #    x = np.cos(np.deg2rad(ang))
        #    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        #    connectionstyle = f"angle,angleA=0,angleB={ang}"
        #    kw["arrowprops"].update({"connectionstyle": connectionstyle})
        #    ax.annotate(recipe[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
        #                horizontalalignment=horizontalalignment, **kw)
        ax.set_title("Phrases by Speaker")

        ax = axs[1][1]
        speaker_labels = list(hits.keys())
        data = list(hits.values())
        if sum(data) == 0:
            data = len(speaker_labels)*[1]
        
        
        ax.pie(data,
               labels=speaker_labels,
               autopct='%1.1f%%',
               textprops={'fontsize': 4}
        )
        ax.set_title("Hits by Speaker")

        ax = axs[2][1]


        with _lock:
            st.pyplot(fig)

        st.write(hits)
