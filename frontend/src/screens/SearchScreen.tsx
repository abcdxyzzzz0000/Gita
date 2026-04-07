import React, { useState, useCallback, useRef } from 'react';
import { View, StyleSheet, FlatList } from 'react-native';
import { Text, Searchbar, Card, Chip, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { RootStackParamList } from '../types/models';
import { searchService, SearchResult } from '../services/searchService';
import { contentService, SemanticSearchResult } from '../services/contentService';
import { theme, spacing } from '../styles/theme';

type SearchNav = NativeStackNavigationProp<RootStackParamList>;

export default function SearchScreen() {
  const navigation = useNavigation<SearchNav>();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [searchMode, setSearchMode] = useState<'keyword' | 'semantic'>('keyword');
  const debounceRef = useRef<NodeJS.Timeout | null>(null);

  const handleSearch = useCallback(
    (text: string) => {
      setQuery(text);

      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }

      if (text.length < 3) {
        setResults([]);
        setSearched(false);
        return;
      }

      debounceRef.current = setTimeout(async () => {
        setLoading(true);
        setSearched(true);
        try {
          if (searchMode === 'semantic') {
            const semanticData = await contentService.semanticSearch(text);
            const mapped: SearchResult[] = semanticData.map((r) => ({
              shloka: r.shloka,
              matched_text: r.shloka.meaning?.substring(0, 80) || '',
              matched_field: `${Math.round(r.relevance_score * 100)}% match`,
            }));
            setResults(mapped);
          } else {
            const data = await searchService.keywordSearch(text);
            setResults(data);
          }
        } catch {
          setResults([]);
        } finally {
          setLoading(false);
        }
      }, 300);
    },
    [searchMode]
  );

  const renderResult = ({ item }: { item: SearchResult }) => (
    <Card
      style={styles.card}
      onPress={() => navigation.navigate('ShlokaDetail', { shlokaId: item.shloka.id })}
    >
      <Card.Content>
        <View style={styles.resultHeader}>
          <Text variant="labelMedium" style={styles.reference}>
            Chapter {item.shloka.chapter}, Verse {item.shloka.shloka_number}
          </Text>
          <Chip compact style={styles.fieldChip} textStyle={styles.fieldChipText}>
            {item.matched_field}
          </Chip>
        </View>
        <Text variant="bodyMedium" style={styles.matchedText} numberOfLines={2}>
          {item.matched_text}
        </Text>
        <Text variant="bodySmall" style={styles.meaning} numberOfLines={1}>
          {item.shloka.meaning}
        </Text>
      </Card.Content>
    </Card>
  );

  return (
    <View style={styles.container}>
      <Searchbar
        placeholder={searchMode === 'semantic' ? 'Describe what you\'re looking for...' : 'Search by keyword, theme, or meaning...'}
        onChangeText={handleSearch}
        value={query}
        style={styles.searchBar}
      />

      <View style={styles.modeRow}>
        <Chip
          selected={searchMode === 'keyword'}
          onPress={() => { setSearchMode('keyword'); if (query.length >= 3) handleSearch(query); }}
          compact
          style={searchMode === 'keyword' ? styles.modeChipActive : styles.modeChip}
        >
          Keyword
        </Chip>
        <Chip
          selected={searchMode === 'semantic'}
          onPress={() => { setSearchMode('semantic'); if (query.length >= 3) handleSearch(query); }}
          compact
          style={searchMode === 'semantic' ? styles.modeChipActive : styles.modeChip}
        >
          Semantic (AI)
        </Chip>
      </View>

      {loading && (
        <View style={styles.loadingRow}>
          <ActivityIndicator size="small" color={theme.colors.primary} />
          <Text variant="bodySmall" style={styles.loadingText}>Searching...</Text>
        </View>
      )}

      {!loading && searched && results.length === 0 && (
        <View style={styles.empty}>
          <Text variant="titleMedium" style={styles.emptyTitle}>
            No results found
          </Text>
          <Text variant="bodyMedium" style={styles.emptyDesc}>
            Try different keywords like "duty", "soul", "peace", or "action"
          </Text>
        </View>
      )}

      {!loading && !searched && (
        <View style={styles.empty}>
          <Text variant="bodyLarge" style={styles.emptyDesc}>
            Search shlokas by keyword, theme, or meaning
          </Text>
          <View style={styles.suggestions}>
            {['duty', 'soul', 'peace', 'action', 'wisdom'].map((s) => (
              <Chip
                key={s}
                compact
                onPress={() => handleSearch(s)}
                style={styles.suggestionChip}
              >
                {s}
              </Chip>
            ))}
          </View>
        </View>
      )}

      <FlatList
        data={results}
        keyExtractor={(item) => item.shloka.id}
        renderItem={renderResult}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
    padding: spacing.md,
  },
  searchBar: {
    marginBottom: spacing.sm,
  },
  modeRow: {
    flexDirection: 'row',
    gap: spacing.sm,
    marginBottom: spacing.md,
  },
  modeChip: {
    backgroundColor: theme.colors.surfaceVariant,
  },
  modeChipActive: {
    backgroundColor: theme.colors.primaryContainer,
  },
  list: {
    paddingBottom: spacing.xl,
  },
  card: {
    marginBottom: spacing.sm,
    backgroundColor: theme.colors.surface,
  },
  resultHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  reference: {
    color: theme.colors.primary,
    fontWeight: '600',
  },
  fieldChip: {
    backgroundColor: theme.colors.surfaceVariant,
    height: 24,
  },
  fieldChipText: {
    fontSize: 10,
  },
  matchedText: {
    color: theme.colors.onSurface,
    lineHeight: 20,
    marginBottom: 4,
  },
  meaning: {
    color: theme.colors.outline,
    fontStyle: 'italic',
  },
  loadingRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.sm,
    marginVertical: spacing.md,
  },
  loadingText: {
    color: theme.colors.outline,
  },
  empty: {
    alignItems: 'center',
    paddingVertical: spacing.xxl,
  },
  emptyTitle: {
    color: theme.colors.primary,
  },
  emptyDesc: {
    color: theme.colors.outline,
    textAlign: 'center',
    marginTop: spacing.sm,
  },
  suggestions: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginTop: spacing.lg,
    justifyContent: 'center',
  },
  suggestionChip: {
    backgroundColor: theme.colors.primaryContainer,
  },
});
