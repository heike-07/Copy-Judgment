import streamlit as st

# 读取TXT文件的内容，返回原文
def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# 逐词对比两个句子的准确性
def compare_sentences(original, duplicate):
    original_words = original.split()
    duplicate_words = duplicate.split()
    correct_count = 0

    # 逐词比较
    for orig_word, dup_word in zip(original_words, duplicate_words):
        if orig_word.lower() == dup_word.lower():
            correct_count += 1

    # 计算准确率
    accuracy = correct_count / len(original_words) if len(original_words) > 0 else 0
    return accuracy

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
        
        # 用户输入的句子
        st.subheader("请在下方输入 Duplicate:")
        user_input = st.text_area("请输入英文句子：")
        
        if user_input:
            # 对比用户输入与原文
            accuracy = compare_sentences(original_text, user_input)
            score = accuracy * 100  # 转换为百分比
            st.subheader(f"输入正确率: {score:.2f}%")

            # 显示反馈
            if accuracy == 1.0:
                st.success("完全正确！")
            elif accuracy > 0.8:
                st.warning("非常接近，稍有错误。")
            else:
                st.error("输入有较大偏差，请重新检查。")

if __name__ == "__main__":
    main()
