"""
OPENAI_ASSITANT
"""

#!/usr/bin/env python
# coding: utf-8

# In[21]:


get_ipython().system('pip install openai')
from pprint import pprint
import json
import time
from openai import OpenAI


# In[6]:


OPEN_AI_KEY="YOUR_API_KEY_HERE"


# In[4]:


client = OpenAI(api_key = OPEN_AI_KEY)


# ### Step 1: Cargar los archivos

# In[7]:


file = client.files.create(
    file=open(r"C:\Users\HP\Desktop\CATO CURSOS-1-2024\GER-TI CATO1-2024\Libros\XXXXXXXXX.pdf","rb"),
    purpose = "assistants"
)

print(file.id)


# In[8]:


file_list = client.files.list()
print(file_list)


# In[9]:


file_id = "file-ED8m2oHKgFq24xLX8WXPAKUu"


# ### Step 2: Crear el asistente

# In[12]:


assistant = client.beta.assistants.create(
    instructions ="Eres un asistente experto en diseño de propuesta de valor para productos nuevos",
    model = "gpt-4-1106-preview",
    tools = [{"type":"retrieval"}],
    file_ids = [file_id]
)


# ### Step 3: Crear el Thread

# In[13]:


thread = client.beta.threads.create()
print(thread)


# ### Step 4: Añadir un mensaje del usuario

# In[14]:


message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role ="user",
    content = " Cual es la porpuesta de valor del yogurt LC1"

)


# ### Step 5: Ejecuta al asistente para obtener la respuesta

# In[18]:


run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id,
    instructions = "Porfavor refierete al usuario como Juanito, si la pregunta no es clara, pide aclracion"
)
print(run.id)


# ### Step 6: Ver el estaus de la ejecución

# In[22]:


while run.status not in["complete","failed"]:
    run = client.beta.threads.runs.retrieve(
    thread_id = thread.id,
    run_id = run.id
    )

    print(run.status)
    time.sleep(10)


# In[ ]:


run_steps = client.beta.threads.runs.steps.list(
    thread_id = thread.id,
    run_id = run.id
)

print(run_steps)


# ### Step 7: Cuando la ejecucion de la consulta esta completada

# In[24]:


messages = client.beta.threads.messages.list(
    thread_id = thread.id
)


# In[25]:


for each in messages:
    pprint(each.role + ":" +each.content[0].text.value)


# ### Step 8: Limpiamos 

# In[28]:


my_assistants = client.beta.assistants.list(
    order="desc",
    limit = "20"
)

print(my_assistants.data)


# In[29]:


response = client.beta.assistants.delete("asst_mFE7WUXXs7oiOK4Tt8Sw2zOb")
print(response)


# In[ ]:




