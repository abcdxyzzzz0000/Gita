import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types/models';
import { useAuthStore } from '../stores/authStore';
import { useBookmarkStore } from '../stores/bookmarkStore';
import { dailyWisdomService, DailyWisdomData } from '../services/dailyWisdomService';
import { theme, spacing } from '../styles/theme';

type HomeNav = NativeStackNavigationProp<RootStackParamList>;

export default function HomeScreen() {
  const navigation = useNavigation<HomeNav>();
  const user = useAuthStore((s) => s.user);
  const fetchBookmarks = useBookmarkStore((s) => s.fetchBookmarks);

  const [wisdom, setWisdom] = useState<DailyWisdomData | null>(null);
  const [wisdomLoading, setWisdomLoading] = useState(true);

  useEffect(() => {
    loadDailyWisdom();
    fetchBookmarks();
  }, []);

  const loadDailyWisdom = async () => {
    try {
      const data = await dailyWisdomService.getDailyWisdom();
      setWisdom(data);
    } catch {
      // silently fail - daily wisdom is non-critical
    } finally {
      setWisdomLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.greeting}>
        <Text variant="headlineMedium" style={styles.welcome}>
          Namaste{user ? `, ${user.email.split('@')[0]}` : ''}
        </Text>
        <Text variant="bodyLarge" style={styles.tagline}>
          Discover timeless wisdom from the Bhagavad Gita
        </Text>
      </View>

      {/* Daily Wisdom */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Daily Wisdom
      </Text>
      {wisdomLoading ? (
        <Card style={styles.wisdomCard}>
          <Card.Content style={styles.wisdomLoading}>
            <ActivityIndicator size="small" color={theme.colors.primary} />
            <Text variant="bodySmall" style={styles.loadingText}>Loading today's wisdom...</Text>
          </Card.Content>
        </Card>
      ) : wisdom ? (
        <Card style={styles.wisdomCard}>
          <Card.Content>
            <Text variant="labelSmall" style={styles.wisdomDate}>
              {new Date(wisdom.date).toLocaleDateString('en-US', {
                weekday: 'long',
                month: 'long',
                day: 'numeric',
              })}
            </Text>
            <Text variant="labelMedium" style={styles.wisdomRef}>
              Chapter {wisdom.chapter}, Verse {wisdom.shloka_number}
            </Text>
            <Text variant="bodyLarge" style={styles.wisdomSanskrit} numberOfLines={2}>
              {wisdom.shloka?.sanskrit_text}
            </Text>
            <Text variant="bodyMedium" style={styles.wisdomMeaning} numberOfLines={3}>
              {wisdom.shloka?.meaning}
            </Text>
            <View style={styles.wisdomDivider} />
            <Text variant="bodySmall" style={styles.wisdomExplanation} numberOfLines={4}>
              {wisdom.explanation}
            </Text>
            {wisdom.shloka?.id && (
              <Button
                mode="text"
                compact
                onPress={() =>
                  navigation.navigate('ShlokaDetail', { shlokaId: wisdom.shloka.id! })
                }
                style={styles.readMore}
              >
                Read More
              </Button>
            )}
          </Card.Content>
        </Card>
      ) : (
        <Card style={styles.card}>
          <Card.Content>
            <Text variant="bodyMedium" style={styles.placeholderText}>
              Daily wisdom will appear here once shloka data is loaded.
            </Text>
          </Card.Content>
        </Card>
      )}

      {/* Quick Actions */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Explore
      </Text>

      <Card style={styles.card} onPress={() => navigation.navigate('MainTabs', { screen: 'Chapters' } as any)}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.cardTitle}>
            Browse All 18 Chapters
          </Text>
          <Text variant="bodySmall" style={styles.cardDesc}>
            Sanskrit text, transliteration, meaning, and AI explanations
          </Text>
        </Card.Content>
      </Card>

      <Card style={styles.card} onPress={() => navigation.navigate('MainTabs', { screen: 'Search' } as any)}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.cardTitle}>
            Search Shlokas
          </Text>
          <Text variant="bodySmall" style={styles.cardDesc}>
            Find verses by keyword, theme, or concept
          </Text>
        </Card.Content>
      </Card>

      <Card style={styles.card} onPress={() => navigation.navigate('LifeGuidance')}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.cardTitle}>
            Life Guidance
          </Text>
          <Text variant="bodySmall" style={styles.cardDesc}>
            Find Gita wisdom for stress, fear, confusion, and more
          </Text>
        </Card.Content>
      </Card>

      <Card style={styles.card} onPress={() => navigation.navigate('Bookmarks')}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.cardTitle}>
            My Bookmarks
          </Text>
          <Text variant="bodySmall" style={styles.cardDesc}>
            Quick access to your saved verses
          </Text>
        </Card.Content>
      </Card>

      <Card style={styles.card} onPress={() => navigation.navigate('WisdomHistory')}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.cardTitle}>
            Wisdom History
          </Text>
          <Text variant="bodySmall" style={styles.cardDesc}>
            Revisit past daily wisdom teachings
          </Text>
        </Card.Content>
      </Card>
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
  greeting: {
    marginBottom: spacing.lg,
    paddingTop: spacing.md,
  },
  welcome: {
    color: theme.colors.primary,
    fontWeight: '700',
  },
  tagline: {
    color: theme.colors.secondary,
    marginTop: spacing.xs,
  },
  sectionTitle: {
    color: theme.colors.primary,
    fontWeight: '600',
    marginBottom: spacing.sm,
    marginTop: spacing.md,
  },
  wisdomCard: {
    marginBottom: spacing.md,
    backgroundColor: theme.colors.secondaryContainer,
  },
  wisdomLoading: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    paddingVertical: spacing.md,
  },
  loadingText: {
    color: theme.colors.outline,
  },
  wisdomDate: {
    color: theme.colors.outline,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  wisdomRef: {
    color: theme.colors.primary,
    fontWeight: '600',
    marginTop: 4,
    marginBottom: spacing.sm,
  },
  wisdomSanskrit: {
    fontFamily: 'serif',
    color: theme.colors.onSurface,
    lineHeight: 26,
    marginBottom: spacing.xs,
  },
  wisdomMeaning: {
    color: theme.colors.onSurface,
    lineHeight: 22,
  },
  wisdomDivider: {
    height: 1,
    backgroundColor: theme.colors.outline,
    opacity: 0.3,
    marginVertical: spacing.sm,
  },
  wisdomExplanation: {
    color: theme.colors.secondary,
    lineHeight: 20,
    fontStyle: 'italic',
  },
  readMore: {
    alignSelf: 'flex-end',
    marginTop: spacing.xs,
  },
  card: {
    marginBottom: spacing.sm,
    backgroundColor: theme.colors.surface,
  },
  cardTitle: {
    color: theme.colors.primary,
    fontWeight: '600',
  },
  cardDesc: {
    color: theme.colors.outline,
    marginTop: 2,
  },
  placeholderText: {
    color: theme.colors.outline,
    fontStyle: 'italic',
  },
});
