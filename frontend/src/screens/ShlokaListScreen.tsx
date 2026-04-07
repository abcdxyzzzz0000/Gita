import React, { useEffect } from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Card, Text, ActivityIndicator } from 'react-native-paper';
import { useRoute, useNavigation, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList, Shloka } from '../types/models';
import { contentService } from '../services/contentService';
import { useContentStore } from '../stores/contentStore';
import { theme, spacing } from '../styles/theme';

type ShlokaListRoute = RouteProp<RootStackParamList, 'ShlokaList'>;

type ShlokaListNav = NativeStackNavigationProp<RootStackParamList, 'ShlokaList'>;

export default function ShlokaListScreen() {
  const route = useRoute<ShlokaListRoute>();
  const navigation = useNavigation<ShlokaListNav>();
  const { chapterId } = route.params;
  const { shlokas, isLoading, setShlokas, setLoading, setError } = useContentStore();

  const chapterShlokas = shlokas[chapterId] || [];

  useEffect(() => {
    if (!shlokas[chapterId]) {
      loadShlokas();
    }
  }, [chapterId]);

  const loadShlokas = async () => {
    setLoading(true);
    try {
      const data = await contentService.getShlokas(chapterId);
      setShlokas(chapterId, data);
    } catch (err: any) {
      setError(err.message || 'Failed to load shlokas');
    }
  };

  const renderShloka = ({ item }: { item: Shloka }) => (
    <Card style={styles.card} onPress={() => navigation.navigate('ShlokaDetail', { shlokaId: item.id })}>
      <Card.Content>
        <Text variant="labelMedium" style={styles.verseRef}>
          Verse {item.shloka_number}
        </Text>
        <Text variant="bodyLarge" style={styles.sanskrit}>
          {item.sanskrit_text}
        </Text>
        <Text variant="bodyMedium" style={styles.transliteration}>
          {item.transliteration}
        </Text>
        <View style={styles.divider} />
        <Text variant="bodyMedium" style={styles.meaning}>
          {item.meaning}
        </Text>
      </Card.Content>
    </Card>
  );

  if (isLoading && chapterShlokas.length === 0) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  return (
    <FlatList
      data={chapterShlokas}
      keyExtractor={(item) => item.id}
      renderItem={renderShloka}
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
    marginBottom: spacing.md,
    backgroundColor: theme.colors.surface,
  },
  verseRef: {
    color: theme.colors.primary,
    fontWeight: '600',
    marginBottom: spacing.sm,
  },
  sanskrit: {
    fontFamily: 'serif',
    lineHeight: 28,
    color: theme.colors.onSurface,
    marginBottom: spacing.sm,
  },
  transliteration: {
    fontStyle: 'italic',
    color: theme.colors.secondary,
    marginBottom: spacing.sm,
    lineHeight: 22,
  },
  divider: {
    height: 1,
    backgroundColor: theme.colors.surfaceVariant,
    marginVertical: spacing.sm,
  },
  meaning: {
    color: theme.colors.onSurface,
    lineHeight: 24,
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.colors.background,
  },
});
