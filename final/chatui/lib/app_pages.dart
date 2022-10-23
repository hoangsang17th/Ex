import 'package:get/get.dart';

import 'auth.binding.dart';
import 'screens/message_screen.dart';

part 'app_routes.dart';

class AppPages {
  static const initial = Routes.chatBot;

  static final routes = [
    GetPage(
      name: Routes.chatBot,
      page: () => const MessagesScreen(),
      bindings: [ChatBinding()],
    ),
  ];
}
