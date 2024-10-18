#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from parcs_stt_tts_msgs.action import TTS
from parcs_stt_tts_msgs.srv import Stop

class ChatbotTTS(Node):

    def __init__(self):
        super().__init__('chatbot_tts')

        self._tts_action_client = ActionClient(self, TTS, 'tts')
        self._goal_in_progress = False

        self._stop_srv_client = self.create_client(Stop, 'stop')
        self.msg = ''
        while not self._stop_srv_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for stop service to become available...')
        self.get_logger().info("Stop service established!")

    def give_input(self, input):
        if input == 'quit' and self._goal_in_progress:
            self.get_logger().info("Pressed stop. Sending service request...")
            self.stop_serv_tts()
            self.msg = ''
        elif not self._goal_in_progress:
            self.msg = input
            self.send_tts_goal(self.msg)
            self.msg = ''
        return

    '''TTS'''
    def send_tts_goal(self, msg):
        goal_msg = TTS.Goal()
        goal_msg.tts = msg

        self.get_logger().info("Waiting for TTS action server...")
        self._tts_action_client.wait_for_server()
        self.get_logger().info("TTS action server found!")

        self._goal_in_progress = True
        self._send_goal_future = self._tts_action_client.send_goal_async(goal_msg, feedback_callback=self.tts_feedback_callback)
        self._send_goal_future.add_done_callback(self.tts_goal_response_callback)

    def tts_goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('TTS goal was rejected.')
            self._goal_in_progress = False
            return
        
        self.get_logger().info('TTS goal accepted, waiting for result...')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.tts_result_callback)

    def tts_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'TTS result received. Said: {result.msg}')
        self._goal_in_progress = False
    
    def tts_feedback_callback(self, feedback_msg):
        self.get_logger().info(f'TTS feedback received: {feedback_msg}')

    '''STOP'''
    def stop_serv_tts(self):
        request = Stop.Request()
        future = self._stop_srv_client.call_async(request)

        future.add_done_callback(self.stop_serv_resp)
    
    def stop_serv_resp(self, future):
        try:
            response = future.result()
            self.get_logger().info(f"Stop service response received. Success: {response.success}")
        except Exception as e:
            self.get_logger().error(f"Stop service call failed: {e}")

def main(args=None):
    rclpy.init(args=args)

    node = ChatbotTTS()

    try: 
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()