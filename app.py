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
    incorrect_count = 0
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
            # 用户未写的单词
            word_results.append(('missing', orig_word))
            incorrect_count += 1

    # 计算准确率和错误率
    accuracy = correct_count / len(original_words) if len(original_words) > 0 else 0
    error_rate = incorrect_count / len(original_words) if len(original_words) > 0 else 0
    return accuracy, error_rate, word_results

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

# Streamlit 界面部分
def main():
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

        # 用来控制计时
        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0  # 初始值

        if 'elapsed_time' not in st.session_state:
            st.session_state.elapsed_time = 0  # 初始值

        # 用于开始写的按钮
        start_button = st.button("开始写")
        
        if start_button:
            # 用户点击“开始写”按钮后开始计时
            st.session_state.start_time = time.time()  # 记录开始时间
            st.session_state.elapsed_time = 0  # 重置已用时间
            st.subheader("请开始输入 Duplicate:")
        
        # 每秒钟更新时间
        if st.session_state.start_time > 0:
            # 显示秒表
            elapsed = time.time() - st.session_state.start_time
            st.session_state.elapsed_time = elapsed
            # st.text(f"秒表: <span style='font-size: 30px; color: black;'>{st.session_state.elapsed_time:.2f} 秒</span>", unsafe_allow_html=True)
            st.markdown(f"秒表: <span style='font-size: 30px; color: black;'>{st.session_state.elapsed_time:.2f} 秒</span>", unsafe_allow_html=True)


        # 用户输入的句子
        user_input = st.text_area("请输入英文句子：", height=150)
        
        # 提交按钮
        submit_button = st.button("提交输入")
        
        if submit_button:
            if user_input.strip():  # 如果用户输入不为空
                end_time = time.time()  # 结束计时
                input_time = end_time - st.session_state.start_time  # 计算输入所需的时间
                
                # 对比用户输入与原文
                accuracy, error_rate, word_results = compare_sentences(original_text, user_input)
                score = accuracy * 100  # 转换为百分比
                error_percentage = error_rate * 100  # 错误率百分比

                # 显示正确率、错误率和逐词结果
                st.subheader(f"输入正确率: {score:.2f}%")
                st.subheader(f"输入错误率: {error_percentage:.2f}%")
                display_comparison_results(word_results)

                # 显示输入时间和速度
                if input_time > 0:  # 确保输入时间大于 0
                    wpm = len(user_input.split()) / (input_time / 60)  # 字/分钟
                    st.subheader(f"输入时间: {input_time:.2f} 秒")
                    st.subheader(f"输入速度: {wpm:.2f} 字/分钟")
                else:
                    st.subheader("输入时间过短，无法计算速度。")

                # 显示反馈
                if accuracy == 1.0:
                    st.success("完全正确！")
                elif accuracy > 0.8:
                    st.warning("非常接近，稍有错误。")
                else:
                    st.error("输入有较大偏差，请重新检查。")
            else:
                st.warning("请输入内容后再点击提交！")

if __name__ == "__main__":
    main()
