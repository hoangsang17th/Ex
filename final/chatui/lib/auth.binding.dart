import 'package:chatui/controllers/chat.controller.dart';
import 'package:get/get.dart';

class ChatBinding extends Bindings {
  @override
  void dependencies() {
    Get.put<ChatController>(
      ChatController(),
      permanent: true,
    );
  }
}
