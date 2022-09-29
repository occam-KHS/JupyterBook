#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os


# In[28]:


loc = 'C:\\Users\\shinki\\Hanbit_Media\\To_Word\\'
files = os.listdir(loc)
files = [f for f in files if ('pdf' in f)]
sorted(files)


# In[29]:


for file in sorted(files):
    if file[-6] == '_':
        os.rename(file, file.replace("_",'_0'))


# In[31]:


from PyPDF2 import PdfMerger

loc = 'C:\\Users\\shinki\\Hanbit_Media\\To_Word\\'
files = os.listdir(loc)
files = [f for f in files if ('pdf' in f)]

merger = PdfMerger()

for pdf in files:
    merger.append(pdf)

merger.write("chapter_all.pdf")
merger.close()


# In[66]:


import aspose.words as aw

loc = 'C:\\Users\\shinki\\Hanbit_Media\\To_Word\\'

doc = aw.Document(loc + 'chapter_all.pdf')
doc.save(loc + "chapter_all.docx")


# In[62]:


print(files)


# In[56]:


# import aspose.words as aw

# # Load source and destination documents
# dstDoc = aw.Document("chapter1_1.docx")
# srcDoc = aw.Document("chapter1_2.docx")

# # Append the source document to the destination document.
# # Pass format mode to retain the original formatting of the source document when importing it.
# dstDoc.append_document(srcDoc, aw.ImportFormatMode.KEEP_SOURCE_FORMATTING)

# # Combine Word documents
# dstDoc.save("chapter2.docx")


# In[ ]:





# In[50]:


# from docx import Document
# files = os.listdir(out_loc)
# files = [f for f in files if 'docx' in f]
# files


# In[51]:


# document = Document()
# document.add_paragraph('chapter2_1.docx')
# document.add_paragraph("chapter2_2.docx")
# document.save("chapter2.docx")


# In[54]:


# from docx import Document
# from docxcompose.composer import Composer
    
# master = Document("chapter2_1.docx")
# composer = Composer(master)
# doc1 = Document("chapter2_2.docx")
# composer.append(doc1)
# master.save('chapter2.docx')


# In[53]:


get_ipython().system('pip install docxcompose')


# In[ ]:




