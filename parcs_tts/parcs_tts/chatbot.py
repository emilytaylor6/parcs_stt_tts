#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from parcs_tts.parcs_tts.chatbot_tts import ChatbotTTS

class Chatbot(Node):

    def __init__(self):
        super().__init__('chatbot')

        tts = ChatbotTTS()

        tts.give_input('hello')

def main(args=None):
    rclpy.init(args=args)

    node = Chatbot()

    try: 
        rclpy.spin(node)
    
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()