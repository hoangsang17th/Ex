import 'dart:convert';

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
    var url = Uri.parse('http://192.168.1.7:3000/chatbot');
    var response = await http.post(url, body: {
      'message': message.text,
    });
    addMsg(message.text, true);
    addMsg(jsonDecode(response.body)['message'], false);
    message.text = "";
  }

  void addMsg(String text, bool isSender) {
    chat.add(ChatMessage(text: text, isSender: isSender));
    chat.refresh();
  }
}
