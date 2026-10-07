import streamlit as st
import random
import time

# -----------------------------
# 기본 설정
# -----------------------------
ROWS = 10
COLS = 17
GAME_TIME = 60

st.set_page_config(
    page_title="🍎 사과게임",
    page_icon="🍎",
    layout="centered"
)

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "board" not in st.session_state:
    st.session_state.board = [
        [random.randint(1, 9) for _ in range(COLS)]
        for _ in range(ROWS)
    ]

if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "selected" not in st.session_state:
    st.session_state.selected = []


# -----------------------------
# 게임 초기화
# -----------------------------
def reset_game():
    st.session_state.board = [
        [random.randint(1, 9) for _ in range(COLS)]
        for _ in range(ROWS)
    ]
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.session_state.selected = []


# -----------------------------
# 선택 영역의 합 계산
# -----------------------------
def get_sum(cells):
    total = 0

    for r, c in cells:
        value = st.session_state.board[r][c]

        if value != 0:
            total += value

    return total


# -----------------------------
# 영역 제거
# -----------------------------
def remove_cells(cells):
    count = 0

    for r, c in cells:
        if st.session_state.board[r][c] != 0:
            st.session_state.board[r][c] = 0
            count += 1

    st.session_state.score += count * 10


# -----------------------------
# 제목
# -----------------------------
st.title("🍎 사과게임")

st.write(
    "숫자의 합이 **10**이 되는 영역을 선택해서 사과를 제거하세요!"
)

# -----------------------------
# 남은 시간
# -----------------------------
elapsed = time.time() - st.session_state.start_time
remaining = max(0, GAME_TIME - int(elapsed))

col1, col2 = st.columns(2)

with col1:
    st.metric("🏆 점수", st.session_state.score)

with col2:
    st.metric("⏰ 남은 시간", f"{remaining}초")


# -----------------------------
# 게임 종료
# -----------------------------
if remaining <= 0:
    st.error("⏰ 게임 종료!")

    if st.button("🔄 다시 시작"):
        reset_game()
        st.rerun()

    st.stop()


# -----------------------------
# 게임판
# -----------------------------
st.write("### 게임판")

# HTML/CSS로 게임판 표시
html = """
<style>

.apple-board {
    display: grid;
    grid-template-columns: repeat(17, 42px);
    gap: 3px;
    justify-content: center;
    margin-top: 20px;
}

.apple {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(
        145deg,
        #ff5c5c,
        #d90000
    );

    color: white;
    font-size: 18px;
    font-weight: bold;

    display: flex;
    align-items: center;
    justify-content: center;

    box-shadow:
        2px 2px 4px rgba(0,0,0,0.3);

    user-select: none;
}

.empty {
    width: 42px;
    height: 42px;
}

</style>

<div class="apple-board">
"""

for r in range(ROWS):
    for c in range(COLS):

        value = st.session_state.board[r][c]

        if value == 0:
            html += '<div class="empty"></div>'
        else:
            html += f'<div class="apple">{value}</div>'

html += "</div>"

st.markdown(html, unsafe_allow_html=True)


# -----------------------------
# 행/열 선택 방식
# -----------------------------
st.write("")
st.write("### 🍎 제거할 영역 선택")

st.caption(
    "시작 행/열과 끝 행/열을 입력하면 해당 직사각형 영역을 선택합니다."
)

c1, c2 = st.columns(2)

with c1:
    start_row = st.number_input(
        "시작 행",
        min_value=1,
        max_value=ROWS,
        value=1
    )

    start_col = st.number_input(
        "시작 열",
        min_value=1,
        max_value=COLS,
        value=1
    )

with c2:
    end_row = st.number_input(
        "끝 행",
        min_value=1,
        max_value=ROWS,
        value=1
    )

    end_col = st.number_input(
        "끝 열",
        min_value=1,
        max_value=COLS,
        value=1
    )


if st.button("🍎 사과 제거", use_container_width=True):

    r1 = min(start_row, end_row) - 1
    r2 = max(start_row, end_row) - 1

    c1 = min(start_col, end_col) - 1
    c2 = max(start_col, end_col) - 1

    cells = [
        (r, c)
        for r in range(r1, r2 + 1)
        for c in range(c1, c2 + 1)
    ]

    total = get_sum(cells)

    if total == 10:
        remove_cells(cells)

        st.success(
            f"🍎 성공! {len(cells)}개의 사과를 제거했습니다!"
        )

        st.rerun()

    else:
        st.warning(
            f"❌ 선택한 영역의 합은 {total}입니다. "
            "숫자의 합이 10이 되어야 합니다."
        )


# -----------------------------
# 다시 시작
# -----------------------------
if st.button("🔄 게임 다시 시작"):
    reset_game()
    st.rerun()


# -----------------------------
# 시간 자동 갱신
# -----------------------------
time.sleep(1)
st.rerun()
