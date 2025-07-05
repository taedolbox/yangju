import streamlit as st
from datetime import datetime, timedelta
import json

def daily_worker_eligibility_mobile_app():
    st.markdown(
        "<span style='font-size:22px; font-weight:600;'>🏗️ 일용직 신청 가능 시점 판단 (모바일용)</span>",
        unsafe_allow_html=True
    )
    
    st.markdown(
        "<p style='font-size:16px; font-weight:700; margin-bottom:10px;'>ⓘ 실업급여 도우미는 참고용입니다. 실제 가능 여부는 고용센터 판단을 따릅니다.</p>",
        unsafe_allow_html=True
    )

    today_kst = datetime.utcnow() + timedelta(hours=9)
    input_date = st.date_input("📅 기준 날짜 선택", today_kst.date())

    first_day_prev_month = (input_date.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day = input_date

    cal_dates = []
    current_date = first_day_prev_month
    while current_date <= last_day:
        cal_dates.append(current_date)
        current_date += timedelta(days=1)

    calendar_groups = {}
    for date in cal_dates:
        ym = date.strftime("%Y-%m")
        if ym not in calendar_groups:
            calendar_groups[ym] = []
        calendar_groups[ym].append(date)

    calendar_dates_json = json.dumps([d.strftime("%Y-%m-%d") for d in cal_dates])
    fourteen_days_prior_end = (input_date - timedelta(days=1)).strftime("%Y-%m-%d")
    fourteen_days_prior_start = (input_date - timedelta(days=14)).strftime("%Y-%m-%d")
    next_possible1_date = (input_date.replace(day=1) + timedelta(days=32)).replace(day=1)
    next_possible1_str = next_possible1_date.strftime("%Y-%m-%d")

    calendar_html = "<div id='calendar-container'>"

    for ym, dates in calendar_groups.items():
        year, month = ym.split("-")
        calendar_html += f"<h4>{year}년 {month}월</h4>"
        calendar_html += """
        <div class="calendar-mobile">
            <div class="day-header">일</div>
            <div class="day-header">월</div>
            <div class="day-header">화</div>
            <div class="day-header">수</div>
            <div class="day-header">목</div>
            <div class="day-header">금</div>
            <div class="day-header">토</div>
        """
        start_day_offset = (dates[0].weekday() + 1) % 7
        for _ in range(start_day_offset):
            calendar_html += '<div class="empty-day"></div>'
        for date in dates:
            day_num = date.day
            date_str = date.strftime("%m/%d")
            calendar_html += f'<div class="day" data-date="{date_str}" onclick="toggleDate(this)">{day_num}</div>'
        calendar_html += "</div>"

    calendar_html += """
    </div>
    <div id="resultContainer"></div>

    <style>
    .calendar-mobile {
        display: grid; 
        grid-template-columns: repeat(7, 1fr);
        gap: 3px;
        margin-bottom: 20px; 
        background: #fff; 
        padding: 5px; 
        border-radius: 6px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        justify-content: flex-start;
    }
    .day-header, .empty-day {
        width: 100%;
        aspect-ratio: 1/1;
        line-height: normal;
        text-align: center;
        font-weight: 600;
        color: #555;
        font-size: 12px;
    }
    .day-header { 
        background: #e0e0e0; 
        border-radius: 4px; 
    }
    .empty-day { 
        background: transparent; 
        border: none; 
    }
    .day {
        width: 100%; 
        aspect-ratio: 1/1;
        line-height: normal;
        text-align: center;
        border: 1px solid #ddd; 
        border-radius: 4px; 
        cursor: pointer; 
        user-select: none;
        transition: background 0.1s ease, border 0.1s ease; 
        font-size: 14px; 
        color: #333;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2px;
    }
    .day:hover { background: #f0f0f0; }
    .day.selected { 
        border: 2px solid #2196F3; 
        background: #2196F3; 
        color: #fff; 
        font-weight: bold; 
    }

    #resultContainer {
        color: #121212;
        background: #fff;
        padding: 10px 15px;
        border-radius: 6px;
        box-shadow: 0 0 8px rgba(0,0,0,0.1);
        font-size: 14px;
        line-height: 1.4;
    }
    #resultContainer h3 {
        color: #0d

