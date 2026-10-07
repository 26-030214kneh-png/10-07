import streamlit as st
import random
import time
import json
import streamlit.components.v1 as components

# ==========================================
# 기본 설정
# ==========================================

ROWS = 10
COLS = 17
GAME_TIME = 60

st.set_page_config(
    page_title="🍎 사과게임",
    page_icon="🍎",
    layout="centered"
)


# ==========================================
# 게임 초기화
# ==========================================

if "board" not in st.session_state:
    st.session_state.board = [
        [random.randint(1, 9) for _ in range(COLS)]
        for _ in range(ROWS)
    ]

if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()


# ==========================================
# 게임 재시작
# ==========================================

if st.button("🔄 새 게임", use_container_width=True):
    st.session_state.board = [
        [random.randint(1, 9) for _ in range(COLS)]
        for _ in range(ROWS)
    ]

    st.session_state.score = 0
    st.session_state.start_time = time.time()

    st.rerun()


# ==========================================
# 시간 계산
# ==========================================

elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, GAME_TIME - elapsed)


# ==========================================
# 상단 정보
# ==========================================

col1, col2 = st.columns(2)

with col1:
    st.metric("🏆 점수", st.session_state.score)

with col2:
    st.metric("⏰ 남은 시간", f"{remaining}초")


st.title("🍎 사과게임")

st.write(
    "마우스로 사과를 **드래그해서 영역을 선택**하세요."
)

st.caption(
    "선택한 사과 숫자의 합이 정확히 10이면 사과가 사라집니다!"
)


# ==========================================
# 게임 종료
# ==========================================

if remaining <= 0:

    st.error("⏰ 게임 종료!")

    st.subheader(f"최종 점수: {st.session_state.score}점")

    st.stop()


# ==========================================
# JavaScript용 게임판 데이터
# ==========================================

board_json = json.dumps(st.session_state.board)


# ==========================================
# HTML + CSS + JavaScript
# ==========================================

html = f"""
<!DOCTYPE html>

<html>

<head>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;

    background: transparent;

    font-family:
        Arial,
        sans-serif;

    user-select: none;
}}


#game-container {{
    width: 100%;

    display: flex;
    justify-content: center;

    padding: 10px;
}}


#board {{

    display: grid;

    grid-template-columns:
        repeat({COLS}, 40px);

    grid-template-rows:
        repeat({ROWS}, 40px);

    gap: 3px;

    position: relative;

    padding: 5px;

    border-radius: 12px;

    background:
        linear-gradient(
            135deg,
            #8bc34a,
            #4caf50
        );

    box-shadow:
        0 5px 15px
        rgba(0,0,0,0.25);

    touch-action: none;

}}


.apple {{

    width: 40px;
    height: 40px;

    border-radius: 50%;

    display: flex;

    align-items: center;
    justify-content: center;

    color: white;

    font-size: 17px;

    font-weight: bold;

    cursor: pointer;

    background:
        radial-gradient(
            circle at 30% 25%,
            #ff8585,
            #f52222 45%,
            #c40000 100%
        );

    box-shadow:
        inset -3px -4px 5px
            rgba(120,0,0,0.35),

        2px 3px 4px
            rgba(0,0,0,0.25);

    transition:
        transform 0.1s,
        opacity 0.2s;

}}


.apple:hover {{
    transform: scale(1.08);
}}


.apple.empty {{
    visibility: hidden;
}}


.apple.selected {{

    background:
        radial-gradient(
            circle,
            #ffd54f,
            #ff9800
        );

    transform: scale(1.08);

    box-shadow:
        0 0 0 3px #fff,

        0 0 12px
        rgba(255,193,7,0.9);

}}


#selection-box {{

    position: absolute;

    border:
        3px solid #2196f3;

    background:
        rgba(33,150,243,0.25);

    pointer-events: none;

    display: none;

    z-index: 100;

}}


#message {{

    text-align: center;

    margin-top: 12px;

    font-size: 18px;

    font-weight: bold;

    min-height: 28px;

}}


.success {{
    color: #2e7d32;
}}

.error {{
    color: #d32f2f;
}}

</style>

</head>


<body>


<div id="game-container">

    <div id="board">

        <div id="selection-box"></div>

    </div>

</div>


<div id="message"></div>


<script>

const boardData = {board_json};

const ROWS = {ROWS};
const COLS = {COLS};


const board =
    document.getElementById("board");

const selectionBox =
    document.getElementById("selection-box");

const message =
    document.getElementById("message");


let startCell = null;

let isDragging = false;


// ========================================
// 게임판 생성
// ========================================

for (let r = 0; r < ROWS; r++) {{

    for (let c = 0; c < COLS; c++) {{

        const apple =
            document.createElement("div");

        apple.className = "apple";

        apple.dataset.row = r;
        apple.dataset.col = c;

        const value = boardData[r][c];

        if (value === 0) {{

            apple.classList.add("empty");

        }} else {{

            apple.textContent = value;

        }}

        board.appendChild(apple);

    }}

}}


// ========================================
// 셀 위치 가져오기
// ========================================

function getCellFromPoint(x, y) {{

    const element =
        document.elementFromPoint(x, y);

    if (!element) return null;

    if (!element.classList.contains("apple"))
        return null;

    return {{
        row: Number(element.dataset.row),
        col: Number(element.dataset.col)
    }};

}}


// ========================================
// 선택된 영역 가져오기
// ========================================

function getCells(r1, c1, r2, c2) {{

    const minRow = Math.min(r1, r2);
    const maxRow = Math.max(r1, r2);

    const minCol = Math.min(c1, c2);
    const maxCol = Math.max(c1, c2);

    const cells = [];

    for (
        let r = minRow;
        r <= maxRow;
        r++
    ) {{

        for (
            let c = minCol;
            c <= maxCol;
            c++
        ) {{

            cells.push([r, c]);

        }}

    }}

    return cells;

}}


// ========================================
// 선택 표시
// ========================================

function showSelection(endCell) {{

    if (!startCell || !endCell)
        return;

    const r1 = startCell.row;
    const c1 = startCell.col;

    const r2 = endCell.row;
    const c2 = endCell.col;

    const minRow = Math.min(r1, r2);
    const maxRow = Math.max(r1, r2);

    const minCol = Math.min(c1, c2);
    const maxCol = Math.max(c1, c2);


    const cells =
        getCells(
            r1,
            c1,
            r2,
            c2
        );


    document
        .querySelectorAll(".apple")
        .forEach(el => {{
            el.classList.remove("selected");
        }});


    let total = 0;

    cells.forEach(([r, c]) => {{

        const index =
            r * COLS + c;

        const apple =
            document.querySelectorAll(
                ".apple"
            )[index];

        if (
            apple &&
            boardData[r][c] !== 0
        ) {{

            apple.classList.add(
                "selected"
            );

            total += boardData[r][c];

        }}

    }});


    // 선택 영역 테두리

    const cellSize = 43;

    selectionBox.style.display = "block";

    selectionBox.style.left =
        (5 + minCol * cellSize) + "px";

    selectionBox.style.top =
        (5 + minRow * cellSize) + "px";

    selectionBox.style.width =
        ((maxCol - minCol + 1) *
        cellSize - 3) + "px";

    selectionBox.style.height =
        ((maxRow - minRow + 1) *
        cellSize - 3) + "px";


    message.className = "";

    message.textContent =
        "선택 영역 합계: " + total;

}}


// ========================================
// 마우스 누르기
// ========================================

board.addEventListener(
    "pointerdown",
    function(e) {{

        const cell =
            getCellFromPoint(
                e.clientX,
                e.clientY
            );

        if (!cell)
            return;

        isDragging = true;

        startCell = cell;

        board.setPointerCapture(
            e.pointerId
        );

        showSelection(cell);

        e.preventDefault();

    }}
);


// ========================================
// 드래그
// ========================================

board.addEventListener(
    "pointermove",
    function(e) {{

        if (!isDragging)
            return;

        const cell =
            getCellFromPoint(
                e.clientX,
                e.clientY
            );

        if (cell) {{

            showSelection(cell);

        }}

        e.preventDefault();

    }}
);


// ========================================
// 마우스 떼기
// ========================================

board.addEventListener(
    "pointerup",
    function(e) {{

        if (!isDragging)
            return;

        isDragging = false;

        const endCell =
            getCellFromPoint(
                e.clientX,
                e.clientY
            );

        if (!startCell || !endCell)
            return;


        const cells =
            getCells(
                startCell.row,
                startCell.col,
                endCell.row,
                endCell.col
            );


        let total = 0;


        cells.forEach(([r, c]) => {{

            if (boardData[r][c] !== 0) {{

                total +=
                    boardData[r][c];

            }}

        }});


        // ====================================
        // 합이 10인 경우
        // ====================================

        if (total === 10) {{

            message.className =
                "success";

            message.textContent =
                "🍎 성공! 사과를 제거합니다!";


            // 선택된 사과 애니메이션

            cells.forEach(([r, c]) => {{

                const index =
                    r * COLS + c;

                const apple =
                    document.querySelectorAll(
                        ".apple"
                    )[index];

                if (apple) {{

                    apple.style.transform =
                        "scale(0)";

                    apple.style.opacity =
                        "0";

                }}

            }});


            // Streamlit에 결과 전달

            const result = {{

                cells: cells,
                total: total

            }};


            window.parent.postMessage(
                {{
                    type:
                        "APPLE_GAME_RESULT",

                    data: result
                }},
                "*"
            );


        }} else {{

            message.className =
                "error";

            message.textContent =
                "❌ 합이 " +
                total +
                "입니다. 10을 만들어주세요!";

        }}


        startCell = null;

        selectionBox.style.display =
            "none";

    }}
);


</script>

</body>

</html>
"""


# ==========================================
# Streamlit에 게임판 표시
# ==========================================

components.html(
    html,
    height=520,
    scrolling=False
)


# ==========================================
# 시간 자동 업데이트
# ==========================================

time.sleep(1)

st.rerun()
