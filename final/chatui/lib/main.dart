import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'app_pages.dart';
import 'theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'Flutter Demo',
      debugShowCheckedModeBanner: false,
      theme: lightThemeData(context),
      navigatorKey: Get.key,
      darkTheme: darkThemeData(context),
      initialRoute: AppPages.initial,
      getPages: AppPages.routes,
    );
  }
}
