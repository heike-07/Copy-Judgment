import streamlit as st
import time
import re

# 读取TXT文件的内容，返回原文
def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# 逐词对比两个句子的准确性
def compare_sentences(original, duplicate):
    original_words = original.split()
    duplicate_words = duplicate.split()
    correct_count = 0
    incorrect_count = 0
    missing_count = 0
    word_results = []

    # 逐词比较
    for i, orig_word in enumerate(original_words):
        if i < len(duplicate_words) and orig_word.lower() == duplicate_words[i].lower():
            word_results.append(('correct', orig_word))
            correct_count += 1
        elif i < len(duplicate_words) and orig_word.lower() != duplicate_words[i].lower():
            word_results.append(('incorrect', orig_word))
            incorrect_count += 1
        else:
            word_results.append(('missing', orig_word))  # 未写的内容
            missing_count += 1

    # 计算准确率和错误率
    accuracy = correct_count / len(original_words) if len(original_words) > 0 else 0
    return accuracy, word_results, correct_count, incorrect_count, missing_count

# 显示逐词对比的结果
def display_comparison_results(word_results):
    # 构建显示结果的HTML
    display_text = ""
    for status, word in word_results:
        if status == 'correct':
            display_text += f'<span style="color: green; font-size: 20px;">{word}</span> '
        elif status == 'incorrect':
            display_text += f'<span style="color: red; font-size: 20px;">{word}</span> '
        else:  # missing word
            display_text += f'<span style="color: gray; font-size: 20px;">{word}</span> '

    st.markdown(display_text, unsafe_allow_html=True)

# 计算有效单词数（忽略标点符号和空格）
def count_words(text):
    words = re.findall(r'\b\w+\b', text)  # 使用正则表达式忽略标点符号
    return len(words)

# Streamlit 界面部分
def main():
    # 初始化session_state
    if 'is_started' not in st.session_state:
        st.session_state.is_started = False
    if 'is_submitted' not in st.session_state:
        st.session_state.is_submitted = False

    # 标题
    st.title("英文句子输入正确率检测")

    # 上传文件
    st.header("上传文件 (TXT 格式)")
    uploaded_file = st.file_uploader("选择一个 TXT 文件", type="txt")
    
    if uploaded_file is not None:
        # 读取并显示文件内容
        original_text = uploaded_file.getvalue().decode("utf-8")
        st.subheader("原文 (Original):")
        st.write(original_text)
        
        # 显示“开始记录”按钮
        if not st.session_state.is_started:
            if st.button("开始记录"):
                st.session_state.is_started = True  # 开始记录后，显示输入框
                st.session_state.start_time = time.time()  # 记录开始时间

        # 用户输入的句子
        if st.session_state.is_started and not st.session_state.is_submitted:  # 只有在点击开始记录后显示输入框
            st.subheader("请在下方输入 Duplicate:")
            user_input = st.text_area("请输入英文句子：", disabled=st.session_state.is_submitted)  # 禁用输入框（提交后）

            # 提交按钮
            if st.button("提交输入", disabled=st.session_state.is_submitted):
                end_time = time.time()  # 结束计时
                input_time = end_time - st.session_state.start_time  # 计算输入所需的时间

                # 对比用户输入与原文
                accuracy, word_results, correct_count, incorrect_count, missing_count = compare_sentences(original_text, user_input)
                score = accuracy * 100  # 转换为百分比

                # 显示正确率和逐词结果
                st.subheader(f"输入正确率: {score:.2f}%")
                display_comparison_results(word_results)

                # 计算有效单词数
                valid_word_count = count_words(user_input)

                # 显示输入时间和速度
                wpm = valid_word_count / (input_time / 60) if input_time > 0 else 0
                st.subheader(f"输入时间: {input_time:.2f} 秒")
                st.subheader(f"输入速度: {wpm:.2f} 字/分钟")

                # 显示反馈
                if accuracy == 1.0:
                    st.success("完全正确！")
                elif accuracy > 0.8:
                    st.warning("非常接近，稍有错误。")
                else:
                    st.error("输入有较大偏差，请重新检查。")

                # 显示错误统计
                st.subheader(f"正确的单词数: {correct_count}")
                st.subheader(f"错误的单词数: {incorrect_count}")
                st.subheader(f"未输入的单词数: {missing_count}")

                # 设置已提交标记
                st.session_state.is_submitted = True

            # 启动计时
            if st.session_state.is_started and not st.session_state.is_submitted:
                st.session_state.start_time = time.time()  # 记录开始时间

        # 提示：如果需要重新记录，刷新页面即可
        if st.session_state.is_submitted:
            st.info("如果需要重新记录，刷新页面即可。")

if __name__ == "__main__":
    main()
