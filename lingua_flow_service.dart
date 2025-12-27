// Passo 5: Servico para integracao com API FastAPI
import 'package:http/http.dart' as http;
import 'dart:convert';

class LinguaFlowService {
  static const String API_URL = 'https://linguaflow-api.onrender.com';
  static const String SESSION_ID = 'flutter_session';

  // POST /chat - Enviar mensagem de texto
  static Future<Map<String, dynamic>> sendMessage(String message) async {
    try {
      final response = await http.post(
        Uri.parse('$API_URL/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'session_id': SESSION_ID,
          'message': message,
        }),
      ).timeout(Duration(seconds: 30));

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Erro ${response.statusCode}: ${response.body}');
      }
    } catch (e) {
      throw Exception('Erro ao enviar mensagem: $e');
    }
  }

  // POST /chat/audio - Enviar audio para transcricao
  static Future<Map<String, dynamic>> sendAudio(List<int> audioBytes) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$API_URL/chat/audio'),
      );

      request.fields['session_id'] = SESSION_ID;
      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          audioBytes,
          filename: 'audio.wav',
        ),
      );

      var streamedResponse = await request.send().timeout(
        Duration(seconds: 60),
      );

      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception('Erro ${response.statusCode}: ${response.body}');
      }
    } catch (e) {
      throw Exception('Erro ao enviar audio: $e');
    }
  }

  // Verificar saude da API
  static Future<bool> healthCheck() async {
    try {
      final response = await http
          .get(Uri.parse('$API_URL/'))
          .timeout(Duration(seconds: 10));
      return response.statusCode == 200;
    } catch (e) {
      print('Health check falhou: $e');
      return false;
    }
  }
}

// Exemplo de uso em um Widget:
// void _sendMessage() async {
//   try {
//     var response = await LinguaFlowService.sendMessage(messageController.text);
//     setState(() {
//       chatResponse = response['response'] ?? 'Sem resposta';
//     });
//   } catch (e) {
//     setState(() {
//       chatResponse = 'Erro: $e';
//     });
//   }
// }
