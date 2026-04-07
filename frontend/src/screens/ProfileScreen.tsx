import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Button, Card, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { useAuthStore } from '../stores/authStore';
import { useBookmarkStore } from '../stores/bookmarkStore';
import { profileService, ProfileStats } from '../services/profileService';
import { RootStackParamList } from '../types/models';
import { theme, spacing } from '../styles/theme';

type ProfileNav = NativeStackNavigationProp<RootStackParamList>;

export default function ProfileScreen() {
  const navigation = useNavigation<ProfileNav>();
  const { user, logout } = useAuthStore();
  const bookmarkCount = useBookmarkStore((s) => s.bookmarks.length);

  const [stats, setStats] = useState<ProfileStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setLoading(true);
    try {
      const data = await profileService.getProfile();
      setStats(data.stats);
    } catch {
      // Use local bookmark count as fallback
      setStats({
        bookmark_count: bookmarkCount,
        shlokas_read: 0,
        chapters_completed: 0,
        days_active: 0,
      });
    } finally {
      setLoading(false);
    }
  };

  const statItems = [
    { label: 'Bookmarks', value: stats?.bookmark_count ?? bookmarkCount, icon: 'bookmark' },
    { label: 'Verses Read', value: stats?.shlokas_read ?? 0, icon: 'book-open-variant' },
    { label: 'Chapters', value: stats?.chapters_completed ?? 0, icon: 'format-list-numbered' },
    { label: 'Days Active', value: stats?.days_active ?? 0, icon: 'calendar-check' },
  ];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* User Info */}
      <Card style={styles.card}>
        <Card.Content style={styles.userSection}>
          <View style={styles.avatar}>
            <Text variant="headlineLarge" style={styles.avatarText}>
              {user?.email?.charAt(0).toUpperCase() || '?'}
            </Text>
          </View>
          <View style={styles.userInfo}>
            <Text variant="titleLarge" style={styles.name}>
              {user?.email.split('@')[0]}
            </Text>
            <Text variant="bodyMedium" style={styles.email}>
              {user?.email}
            </Text>
            <Text variant="bodySmall" style={styles.joined}>
              Joined {user?.created_at ? new Date(user.created_at).toLocaleDateString() : ''}
            </Text>
          </View>
        </Card.Content>
      </Card>

      {/* Stats Grid */}
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Your Progress
      </Text>
      {loading ? (
        <ActivityIndicator style={styles.loader} color={theme.colors.primary} />
      ) : (
        <View style={styles.statsGrid}>
          {statItems.map((item) => (
            <Card key={item.label} style={styles.statCard}>
              <Card.Content style={styles.statContent}>
                <Text variant="headlineMedium" style={styles.statValue}>
                  {item.value}
                </Text>
                <Text variant="labelSmall" style={styles.statLabel}>
                  {item.label}
                </Text>
              </Card.Content>
            </Card>
          ))}
        </View>
      )}

      {/* Quick Links */}
      <Button
        mode="outlined"
        icon="bookmark-multiple"
        onPress={() => navigation.navigate('Bookmarks' as any)}
        style={styles.linkButton}
        contentStyle={styles.linkContent}
      >
        View All Bookmarks ({stats?.bookmark_count ?? bookmarkCount})
      </Button>

      <Button
        mode="outlined"
        icon="chart-line-variant"
        onPress={() => navigation.navigate('ReadingProgress' as any)}
        style={styles.linkButton}
        contentStyle={styles.linkContent}
      >
        Reading Progress
      </Button>

      <Button
        mode="outlined"
        icon="cog"
        onPress={() => navigation.navigate('Settings' as any)}
        style={styles.linkButton}
        contentStyle={styles.linkContent}
      >
        Settings
      </Button>

      <Button
        mode="outlined"
        onPress={logout}
        style={styles.logoutButton}
        textColor={theme.colors.error}
        contentStyle={styles.linkContent}
      >
        Sign Out
      </Button>
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
  },
  card: {
    marginBottom: spacing.lg,
    backgroundColor: theme.colors.surface,
  },
  userSection: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatar: {
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: theme.colors.primaryContainer,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  avatarText: {
    color: theme.colors.primary,
    fontWeight: '700',
  },
  userInfo: {
    flex: 1,
  },
  name: {
    color: theme.colors.onSurface,
    fontWeight: '700',
  },
  email: {
    color: theme.colors.secondary,
    marginTop: 2,
  },
  joined: {
    color: theme.colors.outline,
    marginTop: 2,
  },
  sectionTitle: {
    color: theme.colors.primary,
    fontWeight: '600',
    marginBottom: spacing.md,
  },
  loader: {
    marginVertical: spacing.xl,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.lg,
  },
  statCard: {
    width: '48%',
    backgroundColor: theme.colors.surface,
  },
  statContent: {
    alignItems: 'center',
    paddingVertical: spacing.md,
  },
  statValue: {
    color: theme.colors.primary,
    fontWeight: '700',
  },
  statLabel: {
    color: theme.colors.outline,
    marginTop: 4,
    textTransform: 'uppercase',
  },
  linkButton: {
    marginBottom: spacing.md,
    borderColor: theme.colors.outline,
  },
  linkContent: {
    paddingVertical: 4,
  },
  logoutButton: {
    marginTop: spacing.sm,
    borderColor: theme.colors.error,
  },
});
