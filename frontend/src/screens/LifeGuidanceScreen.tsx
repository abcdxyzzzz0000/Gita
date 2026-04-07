import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView, FlatList } from 'react-native';
import { Text, Card, Chip, ActivityIndicator, Button } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types/models';
import {
  lifeGuidanceService,
  ProblemCategory,
  Recommendation,
} from '../services/lifeGuidanceService';
import { theme, spacing } from '../styles/theme';

type GuidanceNav = NativeStackNavigationProp<RootStackParamList>;

export default function LifeGuidanceScreen() {
  const navigation = useNavigation<GuidanceNav>();
  const [problems, setProblems] = useState<ProblemCategory[]>([]);
  const [selectedProblem, setSelectedProblem] = useState<string | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadProblems();
  }, []);

  const loadProblems = async () => {
    try {
      const data = await lifeGuidanceService.getProblems();
      setProblems(data);
    } catch {}
  };

  const selectProblem = async (problemId: string) => {
    setSelectedProblem(problemId);
    setLoading(true);
    try {
      const data = await lifeGuidanceService.getRecommendations(problemId);
      setRecommendations(data);
    } catch {
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text variant="headlineSmall" style={styles.title}>
        Life Guidance
      </Text>
      <Text variant="bodyMedium" style={styles.subtitle}>
        What are you going through? Select a topic to find relevant Gita wisdom.
      </Text>

      {/* Problem Categories */}
      <View style={styles.chipRow}>
        {problems.map((p) => (
          <Chip
            key={p.id}
            selected={selectedProblem === p.id}
            onPress={() => selectProblem(p.id)}
            style={[
              styles.chip,
              selectedProblem === p.id && styles.chipSelected,
            ]}
            textStyle={selectedProblem === p.id ? styles.chipTextSelected : undefined}
          >
            {p.title}
          </Chip>
        ))}
      </View>

      {/* Results */}
      {loading && (
        <View style={styles.loadingSection}>
          <ActivityIndicator size="large" color={theme.colors.primary} />
          <Text variant="bodySmall" style={styles.loadingText}>
            Finding relevant wisdom...
          </Text>
        </View>
      )}

      {!loading && recommendations.length > 0 && (
        <View>
          <Text variant="titleMedium" style={styles.resultsTitle}>
            Recommended Verses
          </Text>
          {recommendations.map((rec, idx) => (
            <Card
              key={rec.shloka.id}
              style={styles.recCard}
              onPress={() =>
                navigation.navigate('ShlokaDetail', { shlokaId: rec.shloka.id })
              }
            >
              <Card.Content>
                <View style={styles.recHeader}>
                  <Text variant="labelMedium" style={styles.recRef}>
                    Chapter {rec.shloka.chapter}, Verse {rec.shloka.shloka_number}
                  </Text>
                  <Chip compact style={styles.scoreChip} textStyle={styles.scoreText}>
                    {Math.round(rec.relevance_score * 100)}% match
                  </Chip>
                </View>
                <Text variant="bodyMedium" style={styles.recMeaning} numberOfLines={3}>
                  {rec.shloka.meaning}
                </Text>
                <Text variant="bodySmall" style={styles.recExplanation} numberOfLines={3}>
                  {rec.explanation}
                </Text>
              </Card.Content>
            </Card>
          ))}
        </View>
      )}

      {!loading && selectedProblem && recommendations.length === 0 && (
        <View style={styles.empty}>
          <Text variant="bodyMedium" style={styles.emptyText}>
            No recommendations found. Try building the FAISS index first.
          </Text>
        </View>
      )}
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
  title: {
    color: theme.colors.primary,
    fontWeight: '700',
  },
  subtitle: {
    color: theme.colors.secondary,
    marginTop: spacing.xs,
    marginBottom: spacing.lg,
  },
  chipRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  chip: {
    backgroundColor: theme.colors.surfaceVariant,
  },
  chipSelected: {
    backgroundColor: theme.colors.primary,
  },
  chipTextSelected: {
    color: theme.colors.onPrimary,
  },
  loadingSection: {
    alignItems: 'center',
    paddingVertical: spacing.xxl,
  },
  loadingText: {
    color: theme.colors.outline,
    marginTop: spacing.sm,
  },
  resultsTitle: {
    color: theme.colors.primary,
    fontWeight: '600',
    marginBottom: spacing.md,
  },
  recCard: {
    marginBottom: spacing.md,
    backgroundColor: theme.colors.surface,
  },
  recHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  recRef: {
    color: theme.colors.primary,
    fontWeight: '600',
  },
  scoreChip: {
    backgroundColor: theme.colors.primaryContainer,
    height: 24,
  },
  scoreText: {
    fontSize: 10,
    color: theme.colors.primary,
  },
  recMeaning: {
    color: theme.colors.onSurface,
    lineHeight: 22,
    marginBottom: spacing.sm,
  },
  recExplanation: {
    color: theme.colors.secondary,
    fontStyle: 'italic',
    lineHeight: 20,
  },
  empty: {
    alignItems: 'center',
    paddingVertical: spacing.xxl,
  },
  emptyText: {
    color: theme.colors.outline,
  },
});
