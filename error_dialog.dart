import 'package:flutter/material.dart';

class ErrorDialog extends StatelessWidget {
  final String title;
  final String message;

  const ErrorDialog({
    super.key,
    this.title = 'Atenção',
    required this.message,
  });

  // Método estático para exibir o alerta rapidamente de qualquer lugar
  static void show(BuildContext context, String errorMessage) {
    showDialog(
      context: context,
      builder: (ctx) => ErrorDialog(message: errorMessage),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      title: Row(
        children: [
          const Icon(Icons.error_outline, color: Colors.red),
          const SizedBox(width: 10),
          Text(title),
        ],
      ),
      content: Text(
        message,
        style: const TextStyle(fontSize: 16),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('OK', style: TextStyle(fontWeight: FontWeight.bold)),
        ),
      ],
    );
  }
}