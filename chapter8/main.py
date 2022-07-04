import streamlit as st
import datetime
import stock_selection # 종목 추천 모듈을 불러옴

if __name__ == '__main__':

    st.title('코스닥 주식 어드바이저')
    time_now = datetime.datetime.now()
    st.text(time_now)
    st.text(
        "- 장이 끝난 후 조회해야 오늘 정보가 활용됩니다.\n"
        "- 코스닥 전 종목을 분석하므로 결과까지 15분 이상 필요합니다.\n"
        "- 아래 추천 종목의 차트와 뉴스등을 종합적으로 고려하여 매수 결정을 합니다.\n"
        "- yhat 은 다음 5 영업일 이내로 주가가 급등할 확률입니다.\n"
        "- 예약매수 혹은 매수감시 기능을 활용하여 제안된 매수가격(buy_price)에 익일 매수합니다.\n")

    decision_date = st.text_input("오늘 날짜를 다음과 같은 포맷으로 입력하세요. 포맷:  YYYY-MM-DD")

    if decision_date:

        results = stock_selection.select_stocks(decision_date)
        results.rename(columns={'close':'buy_price'}, inplace=True)
        st.write(results.sort_values(by='yhat', ascending=False).head(5))


