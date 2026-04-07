import React, { useEffect, useState } from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Text, Card, ActivityIndicator, IconButton } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types/models';
import {
  dailyWisdomService,
  DailyWisdomData,
} from '../services/dailyWisdomService';
import { theme, spacing } from '../styles/theme';

type HistoryNav = NativeStackNavigationProp<RootStackParamList>;

export default function WisdomHistoryScreen() {
  const navigation = useNavigation<HistoryNav>();
  const [entries, setEntries] = useState<DailyWisdomData[]>([]);
  const [loading, setLoading] = useState(true);
  const [daysBack, setDaysBack] = useState(0);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setLoading(true);
    try {
      // Load last 7 days
      const promises: Promise<DailyWisdomData>[] = [];
      for (let i = 0; i < 7; i++) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        const dateStr = d.toISOString().split('T')[0];
        promises.push(
          dailyWisdomService.getDailyWisdom(dateStr).catch(() => null as any)
        );
      }
      const results = await Promise.all(promises);
      setEntries(results.filter(Boolean));
    } catch {}
    setLoading(false);
  };

  const renderEntry = ({ item }: { item: DailyWisdomData }) => (
    <Card
      style={styles.card}
      onPress={() => {
        if (item.shloka?.id) {
          navigation.navigate('ShlokaDetail', { shlokaId: item.shloka.id });
        }
      }}
    >
      <Card.Content>
        <Text variant="labelSmall" style={styles.date}>
          {new Date(item.date).toLocaleDateString('en-US', {
            weekday: 'long',
            month: 'short',
            day: 'numeric',
          })}
        </Text>
        <Text variant="titleSmall" style={styles.reference}>
          Chapter {item.chapter}, Verse {item.shloka_number}
        </Text>
        <Text variant="bodySmall" style={styles.meaning} numberOfLines={2}>
          {item.shloka?.meaning}
        </Text>
        <Text variant="bodySmall" style={styles.explanation} numberOfLines={2}>
          {item.explanation}
        </Text>
      </Card.Content>
    </Card>
  );

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  if (entries.length === 0) {
    return (
      <View style={styles.centered}>
        <Text variant="bodyLarge" style={styles.emptyText}>
          No wisdom history yet
        </Text>
      </View>
    );
  }

  return (
    <FlatList
      data={entries}
      keyExtractor={(item) => item.id || item.date}
      renderItem={renderEntry}
      contentContainerStyle={styles.list}
      style={styles.container}
    />
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.background },
  list: { padding: spacing.md },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: theme.colors.background },
  emptyText: { color: theme.colors.outline },
  card: { marginBottom: spacing.md, backgroundColor: theme.colors.surface },
  date: { color: theme.colors.outline, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 4 },
  reference: { color: theme.colors.primary, fontWeight: '600', marginBottom: spacing.xs },
  meaning: { color: theme.colors.onSurface, lineHeight: 20, marginBottom: 4 },
  explanation: { color: theme.colors.secondary, fontStyle: 'italic', lineHeight: 18 },
});
