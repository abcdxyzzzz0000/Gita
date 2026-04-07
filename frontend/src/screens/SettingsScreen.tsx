import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView, Platform } from 'react-native';
import { Text, Switch, Card, Button, ActivityIndicator } from 'react-native-paper';
import { settingsService, UserSettings } from '../services/settingsService';
import { theme, spacing } from '../styles/theme';

export default function SettingsScreen() {
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const data = await settingsService.getSettings();
      setSettings(data);
    } catch {
      setSettings({ notification_enabled: true, notification_time: '08:00' });
    } finally {
      setLoading(false);
    }
  };

  const toggleNotifications = async (enabled: boolean) => {
    if (!settings) return;
    const updated = { ...settings, notification_enabled: enabled };
    setSettings(updated);
    setSaving(true);
    try {
      await settingsService.updateSettings({ notification_enabled: enabled });
    } catch {
      setSettings(settings); // revert
    } finally {
      setSaving(false);
    }
  };

  const updateTime = async (time: string) => {
    if (!settings) return;
    const updated = { ...settings, notification_time: time };
    setSettings(updated);
    setSaving(true);
    try {
      await settingsService.updateSettings({ notification_time: time });
    } catch {
      setSettings(settings);
    } finally {
      setSaving(false);
    }
  };

  const timeOptions = [
    '06:00', '07:00', '08:00', '09:00', '10:00',
    '12:00', '18:00', '20:00', '21:00',
  ];

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
      </View>
    );
  }

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text variant="titleMedium" style={styles.sectionTitle}>
        Notifications
      </Text>

      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.row}>
            <View style={styles.rowText}>
              <Text variant="bodyLarge">Daily Wisdom Notifications</Text>
              <Text variant="bodySmall" style={styles.hint}>
                Receive a meaningful shloka each day
              </Text>
            </View>
            <Switch
              value={settings?.notification_enabled ?? true}
              onValueChange={toggleNotifications}
              color={theme.colors.primary}
            />
          </View>
        </Card.Content>
      </Card>

      {settings?.notification_enabled && (
        <Card style={styles.card}>
          <Card.Content>
            <Text variant="bodyLarge" style={styles.timeLabel}>
              Notification Time
            </Text>
            <Text variant="bodySmall" style={styles.hint}>
              Current: {settings.notification_time}
            </Text>
            <View style={styles.timeGrid}>
              {timeOptions.map((t) => (
                <Button
                  key={t}
                  mode={settings.notification_time === t ? 'contained' : 'outlined'}
                  compact
                  onPress={() => updateTime(t)}
                  style={styles.timeButton}
                  labelStyle={styles.timeButtonLabel}
                >
                  {t}
                </Button>
              ))}
            </View>
          </Card.Content>
        </Card>
      )}

      {saving && (
        <Text variant="bodySmall" style={styles.savingText}>
          Saving...
        </Text>
      )}

      <Text variant="titleMedium" style={[styles.sectionTitle, { marginTop: spacing.xl }]}>
        About
      </Text>
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="bodyMedium">Bhagavad Gita Learning App v1.0.0</Text>
          <Text variant="bodySmall" style={styles.hint}>
            Timeless wisdom for modern life
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
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sectionTitle: {
    color: theme.colors.primary,
    fontWeight: '600',
    marginBottom: spacing.md,
  },
  card: {
    marginBottom: spacing.md,
    backgroundColor: theme.colors.surface,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  rowText: {
    flex: 1,
    marginRight: spacing.md,
  },
  hint: {
    color: theme.colors.outline,
    marginTop: 2,
  },
  timeLabel: {
    marginBottom: 4,
  },
  timeGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginTop: spacing.md,
  },
  timeButton: {
    borderRadius: 8,
  },
  timeButtonLabel: {
    fontSize: 13,
  },
  savingText: {
    color: theme.colors.outline,
    textAlign: 'center',
    fontStyle: 'italic',
  },
});
