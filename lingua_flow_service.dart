// Passo 5: Servico para integracao com API FastAPI
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import 'dart:io';

class LinguaFlowService {
  // Lê a URL da API a partir de uma variável de ambiente definida no build.
  // Usa a URL de produção como padrão se nenhuma for fornecida.
  static const String API_URL = String.fromEnvironment(
    'API_URL',
    defaultValue: 'https://linguaflow-kkfr.onrender.com');
  static const String SESSION_ID = 'flutter_session';

  // Helper para tratar respostas de erro da API de forma amigável
  static void _handleResponseErrors(http.Response response) {
    if (response.statusCode == 200) return;

    String errorMessage = 'Erro no servidor (${response.statusCode})';
    try {
      // Tenta extrair a mensagem de erro detalhada da API (FastAPI usa o campo 'detail')
      final body = jsonDecode(response.body);
      if (body is Map && body['detail'] != null) {
        errorMessage = body['detail'];
      }
    } catch (_) {}
    throw Exception(errorMessage);
  }

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

      _handleResponseErrors(response);
      return jsonDecode(response.body);
    } on SocketException {
      throw Exception('Sem conexão com a internet. Verifique sua rede.');
    } on TimeoutException {
      throw Exception('O servidor demorou muito para responder. Tente novamente.');
    } catch (e) {
      // Remove o prefixo "Exception: " se já existir para exibir apenas a mensagem limpa
      throw Exception(e.toString().replaceAll('Exception: ', ''));
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

      _handleResponseErrors(response);
      return jsonDecode(response.body);
    } on SocketException {
      throw Exception('Sem conexão com a internet. Verifique sua rede.');
    } on TimeoutException {
      throw Exception('O envio do áudio demorou muito. Tente novamente.');
    } catch (e) {
      throw Exception(e.toString().replaceAll('Exception: ', ''));
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
