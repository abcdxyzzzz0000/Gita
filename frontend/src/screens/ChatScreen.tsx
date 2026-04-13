import React, { useState, useRef } from 'react';
import {
  View,
  StyleSheet,
  FlatList,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { Text, TextInput, IconButton, Card, ActivityIndicator } from 'react-native-paper';
import { theme, spacing } from '../styles/theme';
import { chatService, ChatMessage } from '../services/chatService';

let msgId = 0;
const nextId = () => String(++msgId);

export default function ChatScreen() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const flatListRef = useRef<FlatList>(null);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg: ChatMessage = {
      id: nextId(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const result = await chatService.sendMessage(text);
      const botMsg: ChatMessage = {
        id: nextId(),
        role: 'assistant',
        content: result.response,
        passages: result.passages,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch {
      const errMsg: ChatMessage = {
        id: nextId(),
        role: 'assistant',
        content: 'Sorry, I could not process your question. Please make sure the backend is running.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  const renderMessage = ({ item }: { item: ChatMessage }) => {
    const isUser = item.role === 'user';
    return (
      <View style={[styles.msgRow, isUser ? styles.msgRowUser : styles.msgRowBot]}>
        <View style={[styles.bubble, isUser ? styles.bubbleUser : styles.bubbleBot]}>
          <Text
            variant="bodyMedium"
            style={[styles.msgText, isUser ? styles.msgTextUser : styles.msgTextBot]}
          >
            {item.content}
          </Text>
        </View>
      </View>
    );
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={90}
    >
      {messages.length === 0 ? (
        <View style={styles.emptyState}>
          <Text variant="headlineSmall" style={styles.emptyTitle}>
            Gita Wisdom Chat
          </Text>
          <Text variant="bodyMedium" style={styles.emptySubtitle}>
            Ask any question about the Bhagavad Gita
          </Text>
          <View style={styles.suggestions}>
            {[
              'What does Krishna say about karma?',
              'How to overcome fear according to Gita?',
              'What is the meaning of dharma?',
              'Explain the concept of detachment',
            ].map((q) => (
              <Card
                key={q}
                style={styles.suggestionCard}
                onPress={() => {
                  setInput(q);
                }}
              >
                <Card.Content>
                  <Text variant="bodySmall" style={styles.suggestionText}>
                    {q}
                  </Text>
                </Card.Content>
              </Card>
            ))}
          </View>
        </View>
      ) : (
        <FlatList
          ref={flatListRef}
          data={messages}
          renderItem={renderMessage}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.messageList}
          onContentSizeChange={() =>
            flatListRef.current?.scrollToEnd({ animated: true })
          }
        />
      )}

      {loading && (
        <View style={styles.typingIndicator}>
          <ActivityIndicator size="small" color={theme.colors.primary} />
          <Text variant="bodySmall" style={styles.typingText}>
            Thinking...
          </Text>
        </View>
      )}

      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          value={input}
          onChangeText={setInput}
          placeholder="Ask about the Bhagavad Gita..."
          placeholderTextColor={theme.colors.outline}
          mode="outlined"
          dense
          onSubmitEditing={sendMessage}
          returnKeyType="send"
          disabled={loading}
          outlineColor={theme.colors.surfaceVariant}
          activeOutlineColor={theme.colors.primary}
        />
        <IconButton
          icon="send"
          iconColor={theme.colors.onPrimary}
          style={[
            styles.sendBtn,
            (!input.trim() || loading) && styles.sendBtnDisabled,
          ]}
          onPress={sendMessage}
          disabled={!input.trim() || loading}
        />
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.lg,
  },
  emptyTitle: {
    color: theme.colors.primary,
    fontWeight: '700',
    marginBottom: spacing.xs,
  },
  emptySubtitle: {
    color: theme.colors.secondary,
    marginBottom: spacing.xl,
  },
  suggestions: {
    width: '100%',
    gap: spacing.sm,
  },
  suggestionCard: {
    backgroundColor: theme.colors.surfaceVariant,
  },
  suggestionText: {
    color: theme.colors.secondary,
  },
  messageList: {
    padding: spacing.md,
    paddingBottom: spacing.sm,
  },
  msgRow: {
    marginBottom: spacing.sm,
    flexDirection: 'row',
  },
  msgRowUser: {
    justifyContent: 'flex-end',
  },
  msgRowBot: {
    justifyContent: 'flex-start',
  },
  bubble: {
    maxWidth: '80%',
    borderRadius: 16,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm + 2,
  },
  bubbleUser: {
    backgroundColor: theme.colors.primary,
    borderBottomRightRadius: 4,
  },
  bubbleBot: {
    backgroundColor: theme.colors.surfaceVariant,
    borderBottomLeftRadius: 4,
  },
  msgText: {
    lineHeight: 22,
  },
  msgTextUser: {
    color: theme.colors.onPrimary,
  },
  msgTextBot: {
    color: theme.colors.onSurface,
  },
  typingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.xs,
    gap: spacing.sm,
  },
  typingText: {
    color: theme.colors.outline,
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.sm,
    paddingBottom: spacing.md,
    borderTopWidth: 1,
    borderTopColor: theme.colors.surfaceVariant,
    backgroundColor: theme.colors.surface,
  },
  input: {
    flex: 1,
    backgroundColor: theme.colors.background,
    fontSize: 15,
  },
  sendBtn: {
    backgroundColor: theme.colors.primary,
    marginLeft: spacing.xs,
  },
  sendBtnDisabled: {
    backgroundColor: theme.colors.outline,
    opacity: 0.5,
  },
});
