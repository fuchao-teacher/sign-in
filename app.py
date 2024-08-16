# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import pandas as pd
import random

app = Flask(__name__)

# 读取题库Excel文件
question_df = pd.read_excel('questions.xlsx')

# 用于存储签到信息的字典
sign_in_data = {}

@app.route('/')
def index():
    # 随机选择一个问题
    question = question_df.sample().iloc[0]
    
    question_text = question['题目']
    options = {
        'A': question['选项A'],
        'B': question['选项B'],
        'C': question['选项C'],
        'D': question['选项D']
    }
    global correct_answer  # 使 correct_answer 在其他函数中可访问
    correct_answer = question['正确答案']

    return render_template('index.html', question=question_text, options=options)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        print(f"接收到的数据: {data}")

        student_name = data.get('name')
        answer = data.get('answer')

        if answer == correct_answer:
            sign_in_data[student_name] = "已签到"
            return jsonify({"status": "success", "message": "签到成功！"})
        else:
            return jsonify({"status": "fail", "message": "答案错误，请再试一次。"})

    except Exception as e:
        print(f"处理请求时出错: {e}")
        return jsonify({"status": "error", "message": f"处理请求时发生错误: {str(e)}"})

@app.route('/results')
def results():
    total_sign_ins = len(sign_in_data)
    return render_template('results.html', total_sign_ins=total_sign_ins, sign_in_data=sign_in_data)

if __name__ == '__main__':
    app.run(debug=True)
