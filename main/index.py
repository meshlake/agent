import sys
from agent.agent import Agent as ML_Agent

config = {
    "situation": "after-sales",
    "actions": [
        {
            "situation": "user describes damaged outer packaging",
            "actions": [
                {
                    "name": "AskForEvidence",
                    "situation": "user describes damaged outer packaging and don't provide any evidence",
                },
                {
                    "name": "NegotiateCompensation",
                    "situation": "user describes damaged outer packaging and provides evidence",
                    "rules": {
                        "compensation": [
                            {"refund_amount": "100"},
                            {"refund_amount": "200"},
                            {"refund_amount": "300"},
                        ]
                    },
                },
                {
                    "name": "StableMessage",
                    "situation": "user agree compensation plan",
                    "rules": {
                        "message": "agree to compensation",
                        "email": {
                            "receiver": "zhaofengnian18@gmail.com",
                            "subject": "用户同意赔偿方案",
                            "content": "请尽快处理用户的赔偿方案",
                        },
                    },
                },
                {
                    "name": "StableMessage",
                    "situation": "user insists on returning the product and has negotiated for compensation more than three",
                    "rules": {"message": "insist on returning the product"},
                },
            ],
        },
        {
            "situation": "user describes wrong delivery",
            "actions": [
                {
                    "name": "AskForEvidence",
                    "situation": "user describes wrong delivery and don't provide any evidence",
                },
                {
                    "name": "NegotiateCompensation",
                    "situation": "user describes wrong delivery and provides evidence",
                    "rules": {
                        "compensation": [
                            {"refund_amount": "100"},
                            {"refund_amount": "200"},
                            {"refund_amount": "300"},
                        ]
                    },
                },
                {
                    "name": "StableMessage",
                    "situation": "user agree compensation plan",
                    "rules": {
                        "message": "agree to compensation",
                        "email": {
                            "receiver": "zhaofengnian18@gmail.com",
                            "subject": "用户同意赔偿方案",
                            "content": "请尽快处理用户的赔偿方案",
                        },
                    },
                },
                {
                    "name": "StableMessage",
                    "situation": "user insists on returning the product and has negotiated for compensation more than three",
                    "rules": {"message": "insist on returning the product"},
                },
            ],
        },
        {
            "situation": "user describes product does not meet expectations",
            "actions": [
                {
                    "name": "AskForEvidence",
                    "situation": "user describes product does not meet expectations and don't provide any evidence",
                },
                {
                    "name": "NegotiateCompensation",
                    "situation": "user describes product does not meet expectations and provides evidence",
                    "rules": {
                        "compensation": [
                            {"refund_amount": "100"},
                            {"refund_amount": "200"},
                            {"refund_amount": "300"},
                        ]
                    },
                },
                {
                    "name": "StableMessage",
                    "situation": "user agree compensation plan",
                    "rules": {
                        "message": "agree to compensation",
                        "email": {
                            "receiver": "zhaofengnian18@gmail.com",
                            "subject": "用户同意赔偿方案",
                            "content": "请尽快处理用户的赔偿方案",
                        },
                    },
                },
                {
                    "name": "StableMessage",
                    "situation": "user insists on returning the product and has negotiated for compensation more than three",
                    "rules": {"message": "insist on returning the product"},
                },
            ],
        },
        {
            "situation": "user describes missing goods",
            "actions": [
                {
                    "name": "AskForEvidence",
                    "situation": "user describes missing goods and don't provide any evidence",
                },
                {
                    "name": "NegotiateCompensation",
                    "situation": "user describes missing goods and provides evidence",
                    "rules": {
                        "compensation": [
                            {"refund_amount": "100"},
                            {"refund_amount": "200"},
                            {"refund_amount": "300"},
                        ]
                    },
                },
                {
                    "name": "StableMessage",
                    "situation": "user agree compensation plan",
                    "rules": {
                        "message": "agree to compensation",
                        "email": {
                            "receiver": "zhaofengnian18@gmail.com",
                            "subject": "用户同意赔偿方案",
                            "content": "请尽快处理用户的赔偿方案",
                        },
                    },
                },
                {
                    "name": "StableMessage",
                    "situation": "user insists on returning the product and has negotiated for compensation more than three",
                    "rules": {"message": "insist on returning the product"},
                },
            ],
        },
    ],
}

# config = {
#     "situation": "damaged outer packaging",
#     "actions": [
#         {
#             "name": "AskForEvidence",
#             "situation": "user describes damaged outer packaging and don't provide any evidence",
#         },
#         {
#             "name": "NegotiateCompensation",
#             "situation": "user describes damaged outer packaging and provides evidence",
#             "rules": {
#                 "compensation": [
#                     {"refund_amount": "100"},
#                     {"refund_amount": "200"},
#                     {"refund_amount": "300"},
#                 ]
#             },
#         },
#         {
#             "name": "StableMessage",
#             "situation": "user agree compensation plan",
#             "rules": {
#                 "message": "agree to compensation",
#                 "email": {
#                     "receiver": "zhaofengnian18@gmail.com",
#                     "subject": "用户同意赔偿方案",
#                     "content": "请尽快处理用户的赔偿方案",
#                 },
#             },
#         },
#         {
#             "name": "StableMessage",
#             "situation": "user insists on returning the product and has negotiated for compensation more than three",
#             "rules": {"message": "insist on returning the product"},
#         },
#     ],
# }

agent = ML_Agent(config)


for line in sys.stdin:
    question = line.strip()
    if "q" == question:
        break
    # The LLM takes a prompt as an input and outputs a completion
    answer = agent.invoke(question)

    print(answer)

# from utils.email_sender import EmailSender

# # 创建EmailSender实例
# email_sender = EmailSender()

# # 替换为你的收件人邮箱、主题和邮件正文
# receiver_email = 'zhaofengnian18@gmail.com'
# subject = 'Test'
# body = 'Test'

# # 发送邮件
# email_sender.send_email(receiver_email, subject, body)
