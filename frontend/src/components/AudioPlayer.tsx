import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { IconButton, Text, ProgressBar } from 'react-native-paper';
import { theme, spacing } from '../styles/theme';

interface AudioPlayerProps {
  shlokaId: string;
  available: boolean;
}

export default function AudioPlayer({ shlokaId, available }: AudioPlayerProps) {
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState(false);

  if (!available) {
    return (
      <View style={styles.container}>
        <Text variant="bodySmall" style={styles.unavailable}>
          Audio not yet available for this verse
        </Text>
      </View>
    );
  }

  const togglePlayback = () => {
    // Audio playback will use expo-av in production
    // For now, show the UI controls
    if (playing) {
      setPlaying(false);
      setProgress(0);
    } else {
      setPlaying(true);
      // Simulate progress for UI demo
      let p = 0;
      const interval = setInterval(() => {
        p += 0.02;
        if (p >= 1) {
          clearInterval(interval);
          setPlaying(false);
          setProgress(0);
          return;
        }
        setProgress(p);
      }, 200);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.controls}>
        <IconButton
          icon={playing ? 'pause-circle' : 'play-circle'}
          iconColor={theme.colors.primary}
          size={40}
          onPress={togglePlayback}
        />
        <View style={styles.progressSection}>
          <ProgressBar
            progress={progress}
            color={theme.colors.primary}
            style={styles.progressBar}
          />
          <Text variant="labelSmall" style={styles.label}>
            {playing ? 'Playing...' : 'Tap to play chanting'}
          </Text>
        </View>
      </View>
      {error && (
        <Text variant="bodySmall" style={styles.error}>
          Unable to play audio
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginVertical: spacing.sm,
  },
  controls: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  progressSection: {
    flex: 1,
    marginRight: spacing.md,
  },
  progressBar: {
    height: 4,
    borderRadius: 2,
  },
  label: {
    color: theme.colors.outline,
    marginTop: 4,
  },
  unavailable: {
    color: theme.colors.outline,
    fontStyle: 'italic',
    textAlign: 'center',
    paddingVertical: spacing.sm,
  },
  error: {
    color: theme.colors.error,
    textAlign: 'center',
  },
});
