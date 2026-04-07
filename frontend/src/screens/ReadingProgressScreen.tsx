import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, ProgressBar, ActivityIndicator } from 'react-native-paper';
import { progressService, ProgressData } from '../services/progressService';
import { theme, spacing } from '../styles/theme';

export default function ReadingProgressScreen() {
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const data = await progressService.getProgress();
      setProgress(data);
    } catch {}
    setLoading(false);
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  if (!progress) {
    return (
      <View style={styles.centered}>
        <Text variant="bodyLarge" style={styles.emptyText}>
          Start reading to see your progress here
        </Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Stats Row */}
      <View style={styles.statsRow}>
        <Card style={styles.statCard}>
          <Card.Content style={styles.statContent}>
            <Text variant="headlineMedium" style={styles.statValue}>
              {progress.total_read}
            </Text>
            <Text variant="labelSmall" style={styles.statLabel}>Verses Read</Text>
          </Card.Content>
        </Card>
        <Card style={styles.statCard}>
          <Card.Content style={styles.statContent}>
            <Text variant="headlineMedium" style={styles.statValue}>
              {progress.streak}
            </Text>
            <Text variant="labelSmall" style={styles.statLabel}>Day Streak</Text>
          </Card.Content>
        </Card>
      </View>

      {/* Continue Reading */}
      {progress.last_read && (
        <Card style={styles.continueCard}>
          <Card.Content>
            <Text variant="titleSmall" style={styles.sectionLabel}>
              Continue Reading
            </Text>
            <Text variant="bodyMedium">
              Chapter {progress.last_read.chapter}, Verse {progress.last_read.shloka_number}
            </Text>
          </Card.Content>
        </Card>
      )}

      {/* Chapter Progress */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Chapter Progress
      </Text>
      {progress.chapter_progress.map((ch) => (
        <View key={ch.chapter} style={styles.chapterRow}>
          <View style={styles.chapterLabel}>
            <Text variant="bodyMedium" style={styles.chapterNum}>
              Ch. {ch.chapter}
            </Text>
            <Text variant="labelSmall" style={styles.chapterCount}>
              {ch.read}/{ch.total}
            </Text>
          </View>
          <View style={styles.progressBarContainer}>
            <ProgressBar
              progress={ch.percentage / 100}
              color={ch.percentage === 100 ? '#4CAF50' : theme.colors.primary}
              style={styles.progressBar}
            />
          </View>
          <Text variant="labelSmall" style={styles.percentage}>
            {ch.percentage}%
          </Text>
        </View>
      ))}

      {/* Recent Reads */}
      {progress.recent.length > 0 && (
        <>
          <Text variant="titleMedium" style={styles.sectionTitle}>
            Recently Read
          </Text>
          {progress.recent.map((r, i) => (
            <Card key={i} style={styles.recentCard}>
              <Card.Content style={styles.recentContent}>
                <Text variant="bodyMedium">
                  Chapter {r.chapter}, Verse {r.shloka_number}
                </Text>
                <Text variant="labelSmall" style={styles.recentDate}>
                  {new Date(r.last_read_at).toLocaleDateString()}
                </Text>
              </Card.Content>
            </Card>
          ))}
        </>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  content: { padding: spacing.lg, paddingBottom: spacing.xxl },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: theme.colors.background },
  emptyText: { color: theme.colors.outline },
  statsRow: { flexDirection: 'row', gap: spacing.sm, marginBottom: spacing.lg },
  statCard: { flex: 1, backgroundColor: theme.colors.surface },
  statContent: { alignItems: 'center', paddingVertical: spacing.md },
  statValue: { color: theme.colors.primary, fontWeight: '700' },
  statLabel: { color: theme.colors.outline, marginTop: 4, textTransform: 'uppercase' },
  continueCard: { marginBottom: spacing.lg, backgroundColor: theme.colors.secondaryContainer },
  sectionLabel: { color: theme.colors.primary, fontWeight: '600', marginBottom: 4 },
  sectionTitle: { color: theme.colors.primary, fontWeight: '600', marginBottom: spacing.md, marginTop: spacing.md },
  chapterRow: { flexDirection: 'row', alignItems: 'center', marginBottom: spacing.sm },
  chapterLabel: { width: 70 },
  chapterNum: { color: theme.colors.onSurface },
  chapterCount: { color: theme.colors.outline },
  progressBarContainer: { flex: 1, marginHorizontal: spacing.sm },
  progressBar: { height: 8, borderRadius: 4 },
  percentage: { width: 40, textAlign: 'right', color: theme.colors.outline },
  recentCard: { marginBottom: spacing.xs, backgroundColor: theme.colors.surface },
  recentContent: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  recentDate: { color: theme.colors.outline },
});
