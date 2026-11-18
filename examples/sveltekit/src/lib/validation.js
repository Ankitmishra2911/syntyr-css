// Standalone validation: the server must still authorize and persist real writes.
export function validateAccountName(entry) {
  if (typeof entry !== 'string') {
    return { value: '', error: 'Enter an account name.' };
  }
  const value = entry.trim();
  if (!value) return { value: '', error: 'Enter an account name.' };
  if (value.length > 80) {
    // Do not echo an unbounded malicious POST body into rendered HTML.
    return { value: value.slice(0, 80), error: 'Use 80 characters or fewer.' };
  }
  if (value.length < 2) {
    return { value, error: 'Use at least 2 characters.' };
  }
  return { value, error: null };
}
