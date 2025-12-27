import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:record/record.dart';
import 'package:path_provider/path_provider.dart';

void main() {
  runApp(const LinguaFlowApp());
}

class LinguaFlowApp extends StatelessWidget {
  const LinguaFlowApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LinguaFlow',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF764BA2),
          primary: const Color(0xFF667EEA),
          secondary: const Color(0xFF764BA2),
        ),
        scaffoldBackgroundColor: const Color(0xFFF8F9FA),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF764BA2),
          foregroundColor: Colors.white,
          elevation: 0,
        ),
      ),
      home: const ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<Map<String, String>> _messages = [
    {'role': 'ai', 'text': 'Hello! I am your English Tutor. How can I help you today?'}
  ];
  final AudioRecorder _audioRecorder = AudioRecorder();
  bool _isLoading = false;
  bool _isRecording = false;
  final String _sessionId = DateTime.now().millisecondsSinceEpoch.toString();

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    _audioRecorder.dispose();
    super.dispose();
  }

  Future<void> _sendMessage() async {
    if (_controller.text.trim().isEmpty) return;

    final userText = _controller.text;
    setState(() {
      _messages.add({'role': 'user', 'text': userText});
      _isLoading = true;
      _controller.clear();
    });

    _scrollToBottom();

    try {
      const apiUrl = String.fromEnvironment('API_URL', defaultValue: 'http://localhost:8000/chat');
      final url = Uri.parse(apiUrl);

      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': userText,
          'session_id': _sessionId,
        }),
      );

      if (response.statusCode == 200 && mounted) {
        final data = jsonDecode(response.body);
        setState(() {
          // Adjust 'response' key based on your API structure
          _messages.add({'role': 'ai', 'text': data['response'] ?? 'No response'});
        });
      } else if (mounted) {
        setState(() {
          _messages.add({'role': 'ai', 'text': 'Error: ${response.statusCode}'});
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _messages.add({'role': 'ai', 'text': 'Connection error. Is the backend running?'});
        });
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
        _scrollToBottom();
      }
    }
  }

  Future<void> _toggleRecording() async {
    try {
      if (await _audioRecorder.isRecording()) {
        final path = await _audioRecorder.stop();
        if (path != null) {
          _sendAudioFile(path);
        }
        setState(() => _isRecording = false);
      } else {
        if (await _audioRecorder.hasPermission()) {
          final directory = await getApplicationDocumentsDirectory();
          final path = '${directory.path}/recording.m4a';
          await _audioRecorder.start(const RecordConfig(), path: path);
          setState(() => _isRecording = true);
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _messages.add({'role': 'ai', 'text': 'Error with microphone: $e'});
        });
      }
    }
  }

  Future<void> _sendAudioFile(String path) async {
    setState(() {
      _isLoading = true;
    });
    _scrollToBottom();

    try {
      const apiUrl = String.fromEnvironment('API_URL', defaultValue: 'http://localhost:8000/chat/audio');
      final url = Uri.parse(apiUrl);

      var request = http.MultipartRequest('POST', url);
      request.fields['session_id'] = _sessionId;
      request.files.add(
        await http.MultipartFile.fromPath('file', path, filename: 'audio.m4a'),
      );

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200 && mounted) {
        final data = jsonDecode(response.body);
        setState(() {
          _messages.add({'role': 'user', 'text': '🎤 ${data['transcription'] ?? 'No transcription'}'});
          _messages.add({'role': 'ai', 'text': data['response'] ?? 'No response'});
        });
      } else if (mounted) {
        setState(() {
          _messages.add({'role': 'ai', 'text': 'Error: ${response.statusCode} - ${response.body}'});
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _messages.add({'role': 'ai', 'text': 'Connection error. Is the backend running?'});
        });
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
        _scrollToBottom();
      }
    }
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LinguaFlow Chat'),
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length + (_isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == _messages.length) {
                  return Align(
                    alignment: Alignment.centerLeft,
                    child: Container(
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: const BorderRadius.only(
                          topLeft: Radius.circular(12),
                          topRight: Radius.circular(12),
                          bottomRight: Radius.circular(12),
                        ),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withValues(alpha: 0.05),
                            blurRadius: 5,
                            offset: const Offset(0, 2),
                          ),
                        ],
                      ),
                      child: const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      ),
                    ),
                  );
                }
                final msg = _messages[index];
                final isUser = msg['role'] == 'user';
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 4),
                    padding: const EdgeInsets.all(12),
                    constraints: BoxConstraints(
                      maxWidth: MediaQuery.of(context).size.width * 0.75,
                    ),
                    decoration: BoxDecoration(
                      color: isUser ? Theme.of(context).colorScheme.primary : Colors.white,
                      borderRadius: BorderRadius.only(
                        topLeft: const Radius.circular(12),
                        topRight: const Radius.circular(12),
                        bottomLeft: isUser ? const Radius.circular(12) : Radius.zero,
                        bottomRight: isUser ? Radius.zero : const Radius.circular(12),
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.05),
                          blurRadius: 5,
                          offset: const Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Text(
                      msg['text']!,
                      style: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                        fontSize: 16,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.all(16.0),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.05),
                  blurRadius: 10,
                  offset: const Offset(0, -5),
                ),
              ],
            ),
            child: Row(
              children: [
                IconButton(
                  onPressed: _toggleRecording,
                  icon: Icon(_isRecording ? Icons.stop : Icons.mic),
                  color: _isRecording ? Colors.red : Theme.of(context).colorScheme.primary,
                  style: IconButton.styleFrom(
                    backgroundColor: _isRecording ? Colors.red.withValues(alpha: 0.5) : Colors.transparent,
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Type a message...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: const Color(0xFFF0F2F5),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 10,
                      ),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  onPressed: _sendMessage,
                  icon: const Icon(Icons.send),
                  style: IconButton.styleFrom(
                    backgroundColor: Theme.of(context).colorScheme.primary,
                    foregroundColor: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
