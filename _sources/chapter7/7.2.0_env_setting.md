# 개발환경

## 계좌개설

모바일 앱 스토에서 Fig 1. 에서 보이는 이베스트 온(eBEST ON) 애플리케이션을 설치 합니다. 
앱 설치 완료 후, 비대면 계좌 개설을 진행 합니다. 
신분증 촬영과 간단한 인증절차를 밟으면 어렵지 않게 계좌 개설을 완료 할 수 있습니다.

```{figure} images/ebeston.png
:width: 600px
:height: 400px
:name: 이베스트 온 애플리케이션

이베스트 온(eBest ON) 애플리케이션 설치
```

## xingAPI 패키지 설치

이어서 Window PC 에 xingAPI 패키지를 설치해야 합니다. 
이베스트투자증권 홈페이지 (http://www.ebestsec.co.kr)로 이동한 후, ID 등록을 진행 합니다. 
ID 등록을 마치면 로그인을 한 상태에서 웹 페이지 하단에 있는 [매매시스템] → [API] 메뉴를 클릭합니다.

```{figure} images/xingAPI_1.png
:width: 600px
:height: 400px
:name: xingAPI 설치

[매매시스템] → [API] 클릭
```

[API] 메뉴 클릭 후, Fig 3 에서 보이는 xingAPI 패키지 PC 버전을 다운 받습니다.

```{figure} images/xingAPI_2.png
:width: 600px
:height: 400px
:name: xingAPI 설치

xingAPI 패키지 PC 버전 설치
```

다운로드한 설치 파일을 더블 클릭해서 설치를 시작합니다. 
Fig 4 와 같이 설치 마법사 화면이 나타나면 [다음] 버튼을 클릭하여 설치를 시작합니다.

```{figure} images/xingAPI_3.png
:width: 600px
:height: 400px
:name: xingAPI 설치

설치 마법사 화면 [다음] 클릭
```

다음으로 기본 설치 경로를 수정하지 말고 [다음] 버튼을 클릭합니다.

```{figure} images/xingAPI_4.png
:width: 600px
:height: 400px
:name: xingAPI 설치

경로 수정하지 않고 [다음] 클릭
```

설치가 완료되면 Fig 6 과 같은 화면이 나타납니다. [완료] 버튼을 눌러 설치 과정을 
종료합니다.

```{figure} images/xingAPI_5.png
:width: 600px
:height: 400px
:name: xingAPI 설치

xingAPI 패키지 설치 [완료] 클릭
```

마지막으로 Fig 7 과 같이  [매매시스템] → [API] → [사용등록/해지] 버튼을 눌러서 인증서 로그인을 진행 합니다. 

```{figure} images/xingAPI_6.png
:width: 600px
:height: 400px
:name: xingAPI 설치

[매매시스템] → [API] → [사용등록/해지] 클릭
```

인증서 로그인을 마치면 Fig 8과 같이 약관에 동의하여 [사용등록] 버튼을 누릅니다. 

```{figure} images/xingAPI_7.png
:width: 600px
:height: 400px
:name: xingAPI 설치

약관 동의 체크 및 [사용등록] 클릭
```

Fig 9와 같이 화면이 나오면 사용자 등록이 완료됩니다.

```{figure} images/xingAPI_8.png
:width: 600px
:height: 400px
:name: xingAPI 설치

사용등록 완료 페이지
```

## DevCenter 에서 Res 파일 다운로드 받기

Res 파일을 Local PC 에 다운 받으면, API 를 통해 증권서버의 데이터를 받을 수 있습니다.
먼저 윈도우 검색창에서 DevCenter 검색 후, 앱을 실행 시킵니다.

```{figure} images/Res_1.png
:width: 600px
:height: 400px
:name: Res 파일 다운로드

윈도우 검색창에서 DevCenter 검색 및 실행 
```

다음으로 데이터베이스 아이콘을 클릭하여 Res 파일을 다운 받습니다.

```{figure} images/Res_2.png
:width: 600px
:height: 400px
:name: Res 파일 다운로드

[아이콘] 클릭
```

다운로드 팝업이 뜨면 예(Y) 버튼을 클릭합니다. 

```{figure} images/Res_3.png
:width: 600px
:height: 400px
:name: Res 파일 다운로드

Res 파일 다운로드 팝업 창 예(Y) 클릭
```

완료 팝업이 뜨면 [확인] 버튼을 클릭하여 Res 파일 다운로드를 완료 합니다.

```{figure} images/Res_4.png
:width: 600px
:height: 400px
:name: Res 파일 다운로드

완료 팝업에서 [확인] 클릭
```

## 모의투자 서비스 가입하기

모의투자 서비스에서 제공하는 가상 투자 환경으로 API 작동 방식을 익히고 알고리즘 백테스팅을 진행 할 수 있습니다. 
아래 Fig 14 와 같이 홈페이지(https://www.ebestsec.co.kr/) 상단에 있는 [고객센터] → [모의투자] → [상시모의투자] 를 클릭해 주세요. 

```{figure} images/mock_1.png
:width: 600px
:height: 400px
:name: 상시 모의투자 가입하기

[고객센터] → [모의투자] → [상시모의투자] 클릭
```

이어서 Fig 15 의 양식에 따라 참가신청을 하면 됩니다. 

```{figure} images/mock_2.png
:width: 600px
:height: 400px
:name: 상시 모의투자 가입하기

양식 채우고 [참가신청] 클릭
```

## 코딩 환경 설치

### 아나콘다 설치

자동매매 코드 작성을 위해 필요한 환경들을 설치하는 시간을 갖겠습니다.
먼저 수백 개의 파이썬 패키지를 한 번에 사용할 수 있는 아나콘다 Anaconda 를 
설치하겠습니다. 
아나콘다 홈페이지(https://www.anaconda.com/products/distribution) 하단에서 
Fig 16 과 같이 [Download] 를 클릭하고,   

```{figure} images/anaconda_1.png
:width: 600px
:height: 400px
:name: 아나콘다 설치

[Download] 클릭
```

Fig 17 에서 32-Bit 버전을 설치합니다.

```{figure} images/anaconda_2.png
:width: 600px
:height: 400px
:name: 아나콘다 설치

Windows 32-Bit 버전 다운받기
```

Fig 18 와 같이 다운로드 받은 아나콘다 설치 파일을 마우스 우클릭하여 관리자 권한으로 실행 합니다. 

```{figure} images/anaconda_3.png
:width: 600px
:height: 400px
:name: 아나콘다 설치

아나콘다 설치 파일 관리자 권한으로 실행 (마우스 우클릭)
```

Fig 19 에서 [Next] 를 클릭하여 아나콘다 설치를 시작합니다.

```{figure} images/anaconda_4.png
:width: 600px
:height: 400px
:name: 아나콘다 설치

아나콘다 설치 시작 화면 [Next] 클릭
```

Fig 20 에서 [I Agree] 를 클릭하여 라이선스 동의서에 동의합니다. 

```{figure} images/anaconda_5.png
:width: 600px
:height: 400px
:name: 아나콘다 설치

라이선스 동의서 [I Agree] 클릭
```

Fig 21 에서 [All Users] 체크 후, [Next] 를 클릭하여 설치 타입을 정합니다.

```{figure} images/anaconda_6.png
:width: 600px
:height: 400px
:name: 아나콘다 설치

[All Users] 타입 체크 및 [Next] 클릭
```

Fig 22 에서 [Next] 를 클릭하여 기본 설치 경로를 따릅니다.

```{figure} images/anaconda_7.png
:width: 600px
:height: 400px
:name: 아나콘다 설치

기본 설치 경로 변경하지 않고 [Next] 클릭
```

Fig 23 과 같이 [Register Anaconda3 as the system Python 3.9] 체크하여 Python IDE에서 인터프리터를 자동 인식 할 수 있도록 설정 합니다. 
체크 후, [Install] 클릭하여 설치를 시작합니다.

```{figure} images/anaconda_8.png
:width: 600px
:height: 400px
:name: 아나콘다 설치

[Register Anaconda3 as the system Python 3.9] 체크 및 [Install] 클릭
```

### PyCharm 설치

파이참 PyCharm 은 파이썬 코드를 실행하고 그 결과를 확인하는 IDE 입니다. (IDE 설명 추가)
Fig 24 와 같이 PyCharm 파이참 홈페이지에서 (https://www.jetbrains.com/ko-kr/pycharm/download/#section=windows) 
Community 버전을 다운 받습니다.

```{figure} images/PyCharm_1.png
:width: 600px
:height: 400px
:name: 파이참 설치

Community 버전 [Download] 클릭
```

다운로드 받은 설치 파일을 실행 시키고 
Fig 25 와 같이 Welcome Page 가 뜨면 [Next] 버튼을 클릭 합니다.

```{figure} images/PyCharm_2.png
:width: 600px
:height: 400px
:name: 파이참 설치

Welcome Page 에서 [Next] 클릭
```

Fig 26 에서는 설치 경로를 설정한 후, [Next] 버튼을 클릭 합니다.

```{figure} images/PyCharm_3.png
:width: 600px
:height: 400px
:name: 파이참 설치

설치 경로 설정 및 [Next] 클릭
```

Fig 27 와 같이 설치 옵션 화면에서 모든 옵션을 선택 후, [Next] 버튼을 클릭 합니다.

```{figure} images/PyCharm_4.png
:width: 600px
:height: 400px
:name: 파이참 설치

모든 옵션 선택 및 [Next] 클릭
```

Fig 28 에서는 시작 메뉴 이름 설정 후, [Install] 버튼을 클릭 합니다.

```{figure} images/PyCharm_5.png
:width: 600px
:height: 400px
:name: 파이참 설치

시작 메뉴 이름 설정 및 [Install] 클릭
```

마지막으로 Fig 29 에서 재부팅을 바로 실행하거나 나중에 실행하기 선택 후 [Finish] 버튼을 클릭 합니다.

```{figure} images/PyCharm_6.png
:width: 600px
:height: 400px
:name: 파이참 설치

재부팅 옵션 선택 및 [Finish] 클릭
```


