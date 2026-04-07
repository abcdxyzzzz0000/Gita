import React, { useEffect, useCallback } from 'react';
import { View, StyleSheet, FlatList, Alert } from 'react-native';
import { Card, Text, ActivityIndicator, IconButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types/models';
import { useBookmarkStore } from '../stores/bookmarkStore';
import { BookmarkData } from '../services/bookmarkService';
import { theme, spacing } from '../styles/theme';

type BookmarkNav = NativeStackNavigationProp<RootStackParamList>;

export default function BookmarksScreen() {
  const navigation = useNavigation<BookmarkNav>();
  const { bookmarks, isLoading, fetchBookmarks, removeBookmark } = useBookmarkStore();

  useEffect(() => {
    fetchBookmarks();
  }, []);

  const handleDelete = useCallback(
    (bookmark: BookmarkData) => {
      Alert.alert(
        'Remove Bookmark',
        `Remove Chapter ${bookmark.chapter}, Verse ${bookmark.shloka_number} from bookmarks?`,
        [
          { text: 'Cancel', style: 'cancel' },
          {
            text: 'Remove',
            style: 'destructive',
            onPress: () => removeBookmark(bookmark.id),
          },
        ]
      );
    },
    [removeBookmark]
  );

  const renderBookmark = ({ item }: { item: BookmarkData }) => (
    <Card
      style={styles.card}
      onPress={() => {
        if (item.shloka?.id) {
          navigation.navigate('ShlokaDetail', { shlokaId: item.shloka.id });
        }
      }}
    >
      <Card.Content style={styles.cardContent}>
        <View style={styles.info}>
          <Text variant="labelMedium" style={styles.reference}>
            Chapter {item.chapter}, Verse {item.shloka_number}
          </Text>
          {item.shloka && (
            <Text variant="bodySmall" style={styles.preview} numberOfLines={2}>
              {item.shloka.meaning}
            </Text>
          )}
          <Text variant="labelSmall" style={styles.date}>
            Saved {new Date(item.created_at).toLocaleDateString()}
          </Text>
        </View>
        <IconButton
          icon="delete-outline"
          iconColor={theme.colors.error}
          size={20}
          onPress={() => handleDelete(item)}
        />
      </Card.Content>
    </Card>
  );

  if (isLoading && bookmarks.length === 0) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  if (bookmarks.length === 0) {
    return (
      <View style={styles.centered}>
        <Text variant="headlineSmall" style={styles.emptyTitle}>
          No bookmarks yet
        </Text>
        <Text variant="bodyMedium" style={styles.emptyDesc}>
          Tap the bookmark icon on any verse to save it here
        </Text>
      </View>
    );
  }

  return (
    <FlatList
      data={bookmarks}
      keyExtractor={(item) => item.id}
      renderItem={renderBookmark}
      contentContainerStyle={styles.list}
      style={styles.container}
      onRefresh={fetchBookmarks}
      refreshing={isLoading}
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
  info: {
    flex: 1,
  },
  reference: {
    color: theme.colors.primary,
    fontWeight: '600',
  },
  preview: {
    color: theme.colors.onSurface,
    marginTop: 4,
    lineHeight: 20,
  },
  date: {
    color: theme.colors.outline,
    marginTop: 4,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.colors.background,
    padding: spacing.xl,
  },
  emptyTitle: {
    color: theme.colors.primary,
  },
  emptyDesc: {
    color: theme.colors.outline,
    marginTop: spacing.sm,
    textAlign: 'center',
  },
});
