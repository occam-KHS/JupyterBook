#!/usr/bin/env python
# coding: utf-8

# ### **WebApp을 배포하자**

# 로컬 환경에서 잘동하는 것을 확인했습니다. 이제 streamlit 에서 제공하는 호스팅을 이용하여 웹앱을 배포해 보겠습니다. 아래와 같은 순서대로 진행하면 됩니다.
# 
# ~~~~
# 1. requirements.txt 파일을 추가합니다 
# 2. 만들어진 WebApp 를 Github 에 Push 합니다.
# 3. https://share.streamlit.io  와 본인의 github repository 를 연결하고 배포합니다.
# ~~~~

# <br></br>
# 1.'requirements.txt' 파일 만들기
# 
# 아나콘다 프롬프트에서 아래와 같이 명령어를 주면 'requirements.txt' 파일이 생성됩니다. 'requirements.txt' 는 Webapp 이 동작하기 위한 모든 라이브러리와 버전 정보가 있습니다.

# ![GET_IMAGE](images/requirements_Streamlit.PNG)

# <br>
# 'requirements.txt' 을 열어서 보면 아래와 같습니다.  이 파일을 main.py 가 있는 폴더에 넣어줍니다. Streamlit 에 Webapp 를 배포하는 과정에 아래 버전이 존재하지 않아 에러가 나는 경우가 있습니다. 이때는 '== 버전' 제거하고 다시 진행을 합니다.

# ![GET_IMAGE](images/requirements_file.PNG)

# <br></br>
# 2. Github 에 Push 하기

# 아래와 같이 'requirements.txt' 파일을 작업폴더에 복사하고 github 에 push 합니다.

# ![GET_IMAGE](images/git_push.PNG)

# <br></br>
# 3. https://share.streamlit.io 에서 배포하기

# share.streamlit.io 에서 github Repository 와 연결한 후, 아래와 같이 Branch 이름과 파이썬 파일을 지정해줍니다. 그리고 Deploy 버튼을 누르면 Webapp 이 만들어 집니다.

# ![GET_IMAGE](images/deploy_app.PNG)

# ![GET_IMAGE](images/webapp_launch.PNG)
