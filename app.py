import streamlit as st
import time

# 读取TXT文件的内容，返回原文
def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# 逐词对比两个句子的准确性
def compare_sentences(original, duplicate):
    original_words = original.split()
    duplicate_words = duplicate.split()
    correct_count = 0
    word_results = []

    # 逐词比较
    for orig_word, dup_word in zip(original_words, duplicate_words):
        if orig_word.lower() == dup_word.lower():
            word_results.append(('correct', orig_word))
            correct_count += 1
        else:
            word_results.append(('incorrect', orig_word))

    # 对比结束后，处理用户没有输入的单词
    if len(duplicate_words) < len(original_words):
        for missing_word in original_words[len(duplicate_words):]:
            word_results.append(('missing', missing_word))

    # 计算准确率
    accuracy = correct_count / len(original_words) if len(original_words) > 0 else 0
    return accuracy, word_results

# 显示逐词对比的结果
def display_comparison_results(word_results):
    # 构建显示结果的HTML
    display_text = ""
    for status, word in word_results:
        if status == 'correct':
            display_text += f'<span style="color: green;">{word}</span> '
        elif status == 'incorrect':
            display_text += f'<span style="color: red;">{word}</span> '
        elif status == 'missing':
            display_text += f'<span style="color: gray;">{word}</span> '
    
    st.markdown(display_text, unsafe_allow_html=True)

# Streamlit 界面部分
def main():
    # 标题
    st.title("英文句子输入正确率检测")
    st.write("@ 作者(Author)：heike07 & ChatGpt4o")

    # 上传文件
    st.header("上传文件 (TXT 格式)")
    uploaded_file = st.file_uploader("选择一个 TXT 文件", type="txt")
    
    if uploaded_file is not None:
        # 读取并显示文件内容
        original_text = uploaded_file.getvalue().decode("utf-8")
        st.subheader("原文 (Original):")
        st.write(original_text)
        
        # 状态管理：记录按钮和输入框状态
        if "is_recording" not in st.session_state:
            st.session_state.is_recording = False  # 初始状态未开始录入

        if "is_submitted" not in st.session_state:
            st.session_state.is_submitted = False  # 初始状态未提交

        if "start_time" not in st.session_state:
            st.session_state.start_time = 0  # 初始时间

        # 开始记录按钮
        start_button = st.button("开始写", disabled=st.session_state.is_recording or st.session_state.is_submitted)
        if start_button:
            st.session_state.is_recording = True  # 开始记录，按钮置灰
            st.session_state.is_submitted = False  # 确保点击开始记录后可以提交
            st.session_state.start_time = time.time()  # 记录开始时间

        # 用户输入的句子
        st.subheader("请在下方输入 Duplicate:")
        user_input = st.text_area("请输入英文句子：", disabled=not st.session_state.is_recording)
        
        # 提交按钮
        submit_button = st.button("我写好了", disabled=not st.session_state.is_recording or st.session_state.is_submitted)
        
        if submit_button:
            # 计算输入所需的时间
            input_time = time.time() - st.session_state.start_time  # 结束时间 - 开始时间

            # 对比用户输入与原文
            accuracy, word_results = compare_sentences(original_text, user_input)
            score = accuracy * 100  # 转换为百分比

            # 显示正确率和逐词结果
            st.subheader(f"输入正确率: {score:.2f}%")
            display_comparison_results(word_results)

            # 显示输入时间和速度
            words_count = len(user_input.split())
            wpm = words_count / (input_time / 60) if input_time > 0 else 0  # 词/分钟
            st.subheader(f"输入时间: {input_time:.2f} 秒")
            st.subheader(f"输入速度: {wpm:.2f} 字符/分钟")

            # 显示反馈
            if accuracy == 1.0:
                st.success("完全正确！")
            elif accuracy > 0.8:
                st.warning("非常接近，稍有错误。")
            else:
                st.error("输入有较大偏差，请重新检查。")

            # 更新状态：提交后禁用相关控件
            st.session_state.is_submitted = True
            st.session_state.is_recording = False  # 禁用输入框

            # 提示用户刷新页面以重新开始
            st.info("如果需要重新记录，请刷新页面。")

if __name__ == "__main__":
    main()
