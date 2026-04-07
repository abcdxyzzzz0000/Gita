import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import {
  Text,
  ActivityIndicator,
  IconButton,
  Chip,
  Card,
  Divider,
} from 'react-native-paper';
import { useRoute, useNavigation, RouteProp } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types/models';
import { contentService, ShlokaDetail } from '../services/contentService';
import { useContentStore } from '../stores/contentStore';
import { useAuthStore } from '../stores/authStore';
import { useBookmarkStore } from '../stores/bookmarkStore';
import AudioPlayer from '../components/AudioPlayer';
import { progressService } from '../services/progressService';
import { theme, spacing } from '../styles/theme';

type DetailRoute = RouteProp<RootStackParamList, 'ShlokaDetail'>;
type DetailNav = NativeStackNavigationProp<RootStackParamList, 'ShlokaDetail'>;

export default function ShlokaDetailScreen() {
  const route = useRoute<DetailRoute>();
  const navigation = useNavigation<DetailNav>();
  const { shlokaId } = route.params;
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const { isBookmarked: checkBookmarked, addBookmark, removeBookmarkByShloka } = useBookmarkStore();

  const [shloka, setShloka] = useState<ShlokaDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [explanationLoading, setExplanationLoading] = useState(false);
  const [error, setError] = useState('');

  // Get sibling shlokas for prev/next navigation
  const { shlokas: allShlokas } = useContentStore();

  useEffect(() => {
    loadShlokaDetail();
  }, [shlokaId]);

  const loadShlokaDetail = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await contentService.getShlokaDetail(shlokaId);
      setShloka(data);
      // Record reading progress if authenticated
      if (isAuthenticated && data) {
        progressService.recordProgress(data.chapter, data.shloka_number).catch(() => {});
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load shloka');
    } finally {
      setLoading(false);
    }
  };

  const getSiblingShlokas = () => {
    if (!shloka) return { prev: null, next: null };
    const chapterShlokas = allShlokas[shloka.chapter] || [];
    const currentIdx = chapterShlokas.findIndex((s) => s.id === shlokaId);
    return {
      prev: currentIdx > 0 ? chapterShlokas[currentIdx - 1] : null,
      next: currentIdx < chapterShlokas.length - 1 ? chapterShlokas[currentIdx + 1] : null,
    };
  };

  const { prev, next } = getSiblingShlokas();

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text variant="bodyMedium" style={styles.loadingText}>
          Loading verse...
        </Text>
      </View>
    );
  }

  if (error || !shloka) {
    return (
      <View style={styles.centered}>
        <Text variant="bodyLarge" style={styles.errorText}>
          {error || 'Shloka not found'}
        </Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Verse Reference */}
      <View style={styles.header}>
        <Text variant="titleLarge" style={styles.reference}>
          Chapter {shloka.chapter}, Verse {shloka.shloka_number}
        </Text>
        {isAuthenticated && shloka && (
          <IconButton
            icon={checkBookmarked(shloka.chapter, shloka.shloka_number) ? 'bookmark' : 'bookmark-outline'}
            iconColor={checkBookmarked(shloka.chapter, shloka.shloka_number) ? theme.colors.primary : theme.colors.outline}
            size={28}
            onPress={() => {
              if (checkBookmarked(shloka.chapter, shloka.shloka_number)) {
                removeBookmarkByShloka(shloka.chapter, shloka.shloka_number);
              } else {
                addBookmark(shloka.chapter, shloka.shloka_number);
              }
            }}
          />
        )}
      </View>

      {/* Sanskrit Text */}
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="labelMedium" style={styles.sectionLabel}>
            Sanskrit
          </Text>
          <Text variant="bodyLarge" style={styles.sanskrit}>
            {shloka.sanskrit_text}
          </Text>
        </Card.Content>
      </Card>

      {/* Transliteration */}
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="labelMedium" style={styles.sectionLabel}>
            Transliteration
          </Text>
          <Text variant="bodyMedium" style={styles.transliteration}>
            {shloka.transliteration}
          </Text>
        </Card.Content>
      </Card>

      {/* English Meaning */}
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="labelMedium" style={styles.sectionLabel}>
            Meaning
          </Text>
          <Text variant="bodyMedium" style={styles.meaning}>
            {shloka.meaning}
          </Text>
        </Card.Content>
      </Card>

      {/* Audio Player */}
      <AudioPlayer
        shlokaId={shlokaId}
        available={!!shloka.audio_file_path}
      />

      {/* AI Explanation */}
      <Card style={styles.explanationCard}>
        <Card.Content>
          <View style={styles.explanationHeader}>
            <Text variant="labelMedium" style={styles.sectionLabel}>
              Simple Explanation
            </Text>
            <Chip
              compact
              textStyle={styles.aiChipText}
              style={styles.aiChip}
            >
              AI-generated
            </Chip>
          </View>
          {shloka.explanation ? (
            <Text variant="bodyMedium" style={styles.explanation}>
              {shloka.explanation}
            </Text>
          ) : (
            <View style={styles.explanationLoading}>
              <ActivityIndicator size="small" color={theme.colors.primary} />
              <Text variant="bodySmall" style={styles.loadingText}>
                Generating explanation...
              </Text>
            </View>
          )}
        </Card.Content>
      </Card>

      {/* Themes */}
      {shloka.themes && shloka.themes.length > 0 && (
        <View style={styles.themes}>
          <Text variant="labelMedium" style={styles.sectionLabel}>
            Themes
          </Text>
          <View style={styles.chipRow}>
            {shloka.themes.map((t) => (
              <Chip key={t} compact style={styles.themeChip} textStyle={styles.themeText}>
                {t}
              </Chip>
            ))}
          </View>
        </View>
      )}

      {/* Prev / Next Navigation */}
      <Divider style={styles.divider} />
      <View style={styles.navRow}>
        {prev ? (
          <IconButton
            icon="chevron-left"
            mode="contained-tonal"
            size={24}
            onPress={() =>
              navigation.replace('ShlokaDetail', { shlokaId: prev.id })
            }
          />
        ) : (
          <View style={{ width: 48 }} />
        )}
        <Text variant="bodySmall" style={styles.navLabel}>
          Verse {shloka.shloka_number} of{' '}
          {allShlokas[shloka.chapter]?.length || '?'}
        </Text>
        {next ? (
          <IconButton
            icon="chevron-right"
            mode="contained-tonal"
            size={24}
            onPress={() =>
              navigation.replace('ShlokaDetail', { shlokaId: next.id })
            }
          />
        ) : (
          <View style={{ width: 48 }} />
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  content: {
    padding: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  reference: {
    color: theme.colors.primary,
    fontWeight: '700',
  },
  card: {
    marginBottom: spacing.md,
    backgroundColor: theme.colors.surface,
  },
  sectionLabel: {
    color: theme.colors.primary,
    fontWeight: '600',
    marginBottom: spacing.sm,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  sanskrit: {
    fontFamily: 'serif',
    lineHeight: 30,
    color: theme.colors.onSurface,
  },
  transliteration: {
    fontStyle: 'italic',
    color: theme.colors.secondary,
    lineHeight: 24,
  },
  meaning: {
    color: theme.colors.onSurface,
    lineHeight: 24,
  },
  explanationCard: {
    marginBottom: spacing.md,
    backgroundColor: theme.colors.secondaryContainer,
  },
  explanationHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  aiChip: {
    backgroundColor: theme.colors.primaryContainer,
    height: 26,
  },
  aiChipText: {
    fontSize: 10,
    color: theme.colors.primary,
  },
  explanation: {
    color: theme.colors.onSurface,
    lineHeight: 24,
  },
  explanationLoading: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    paddingVertical: spacing.md,
  },
  loadingText: {
    color: theme.colors.outline,
    marginTop: spacing.sm,
  },
  errorText: {
    color: theme.colors.error,
  },
  themes: {
    marginBottom: spacing.md,
  },
  chipRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.xs,
  },
  themeChip: {
    backgroundColor: theme.colors.surfaceVariant,
  },
  themeText: {
    fontSize: 12,
  },
  divider: {
    marginVertical: spacing.md,
  },
  navRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  navLabel: {
    color: theme.colors.outline,
  },
});
