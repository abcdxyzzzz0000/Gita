import React, { useEffect } from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Card, Text, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList, Chapter } from '../types/models';
import { contentService } from '../services/contentService';
import { useContentStore } from '../stores/contentStore';
import { theme, spacing } from '../styles/theme';

type ChapterNav = NativeStackNavigationProp<RootStackParamList>;

export default function ChapterListScreen() {
  const navigation = useNavigation<ChapterNav>();
  const { chapters, isLoading, setChapters, setLoading, setError } = useContentStore();

  useEffect(() => {
    if (chapters.length === 0) {
      loadChapters();
    }
  }, []);

  const loadChapters = async () => {
    setLoading(true);
    try {
      const data = await contentService.getChapters();
      setChapters(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load chapters');
    }
  };

  const renderChapter = ({ item }: { item: Chapter }) => (
    <Card
      style={styles.card}
      onPress={() =>
        navigation.navigate('ShlokaList', {
          chapterId: item.id,
          chapterTitle: item.title,
        })
      }
    >
      <Card.Content style={styles.cardContent}>
        <View style={styles.chapterNumber}>
          <Text variant="headlineSmall" style={styles.number}>
            {item.id}
          </Text>
        </View>
        <View style={styles.chapterInfo}>
          <Text variant="titleMedium" style={styles.title}>
            {item.title}
          </Text>
          <Text variant="bodySmall" style={styles.sanskritName}>
            {item.sanskrit_name}
          </Text>
          <Text variant="bodySmall" style={styles.shlokaCount}>
            {item.shloka_count} verses
          </Text>
        </View>
      </Card.Content>
    </Card>
  );

  if (isLoading && chapters.length === 0) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  return (
    <FlatList
      data={chapters}
      keyExtractor={(item) => item.id.toString()}
      renderItem={renderChapter}
      contentContainerStyle={styles.list}
      style={styles.container}
    />
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  list: {
    padding: spacing.md,
  },
  card: {
    marginBottom: spacing.sm,
    backgroundColor: theme.colors.surface,
  },
  cardContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  chapterNumber: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: theme.colors.primaryContainer,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  number: {
    color: theme.colors.primary,
    fontWeight: '700',
  },
  chapterInfo: {
    flex: 1,
  },
  title: {
    color: theme.colors.onSurface,
    fontWeight: '600',
  },
  sanskritName: {
    color: theme.colors.secondary,
    fontStyle: 'italic',
    marginTop: 2,
  },
  shlokaCount: {
    color: theme.colors.outline,
    marginTop: 2,
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.colors.background,
  },
});
