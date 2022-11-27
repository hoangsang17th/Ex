import 'dart:convert';
import 'dart:developer';

import 'package:flutter/cupertino.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;

class ChatMessage {
  final String text;
  final bool isSender;

  ChatMessage({
    this.text = '',
    required this.isSender,
  });
}

class ChatController extends GetxController {
  TextEditingController message = TextEditingController();
  RxList<ChatMessage> chat = <ChatMessage>[].obs;
  Future<void> onSendMsg() async {
    try {
      var url = Uri.parse('http://localhost:3000/chatbot');
      var response = await http.post(url, body: {
        'message': message.text,
      });
      addMsg(message.text, true);
      addMsg(jsonDecode(response.body)['message'], false);
      message.text = "";
    } catch (e) {
      log("Lỗi connect rồi");
    }
  }

  void addMsg(String text, bool isSender) {
    chat.add(ChatMessage(text: text, isSender: isSender));
    chat.refresh();
  }
}
