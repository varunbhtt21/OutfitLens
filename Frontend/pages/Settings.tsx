import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useAuthStore } from '../store/authStore';
import { userApi } from '../lib/api';
import { GlassCard, Input, Button } from '../components/ui/GlassComponents';
import { User as UserIcon, Lock, AlertTriangle } from 'lucide-react';

type Tab = 'profile' | 'security' | 'account';

const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState<Tab>('profile');
  const { user, updateUser, logout } = useAuthStore();
  const navigate = useNavigate();

  // Profile state
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [profileLoading, setProfileLoading] = useState(false);

  // Password state
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordLoading, setPasswordLoading] = useState(false);

  // Delete account state
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileLoading(true);

    try {
      const updated = await userApi.updateProfile({ full_name: fullName });
      updateUser(updated);
      toast.success('Profile updated successfully!');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to update profile');
    } finally {
      setProfileLoading(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordLoading(true);

    if (newPassword !== confirmPassword) {
      toast.error('New passwords do not match');
      setPasswordLoading(false);
      return;
    }

    if (newPassword.length < 8) {
      toast.error('Password must be at least 8 characters');
      setPasswordLoading(false);
      return;
    }

    try {
      await userApi.changePassword({ old_password: oldPassword, new_password: newPassword });
      toast.success('Password changed successfully!');
      setOldPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to change password');
    } finally {
      setPasswordLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    setDeleteLoading(true);
    try {
      await userApi.deleteAccount();
      toast.success('Account deleted successfully');
      logout();
      navigate('/login');
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to delete account');
      setDeleteLoading(false);
    }
  };

  const tabs: { id: Tab; label: string; icon: any }[] = [
    { id: 'profile', label: 'Profile', icon: <UserIcon size={18} /> },
    { id: 'security', label: 'Security', icon: <Lock size={18} /> },
    { id: 'account', label: 'Account', icon: <AlertTriangle size={18} /> },
  ];

  return (
    <div className="max-w-4xl space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-white/10 pb-px">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`
              flex items-center gap-2 px-4 py-2 rounded-t-lg transition-all
              ${activeTab === tab.id
                ? 'bg-white/10 text-white border-b-2 border-brand-purple'
                : 'text-gray-400 hover:text-white hover:bg-white/5'
              }
            `}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'profile' && (
        <GlassCard className="p-6">
          <h2 className="text-xl font-semibold mb-6">Profile Information</h2>

          <form onSubmit={handleUpdateProfile} className="space-y-6">
            <Input
              label="Email Address"
              type="email"
              value={user?.email || ''}
              disabled
              className="bg-white/5 cursor-not-allowed"
            />

            <Input
              label="Full Name"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="John Doe"
              required
            />

            <div className="flex justify-end">
              <Button type="submit" isLoading={profileLoading}>
                Save Changes
              </Button>
            </div>
          </form>
        </GlassCard>
      )}

      {activeTab === 'security' && (
        <GlassCard className="p-6">
          <h2 className="text-xl font-semibold mb-6">Change Password</h2>

          <form onSubmit={handleChangePassword} className="space-y-6">
            <Input
              label="Current Password"
              type="password"
              value={oldPassword}
              onChange={(e) => setOldPassword(e.target.value)}
              placeholder="••••••••"
              required
            />

            <Input
              label="New Password"
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="••••••••"
              required
            />

            <Input
              label="Confirm New Password"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="••••••••"
              required
            />

            <div className="flex justify-end">
              <Button type="submit" isLoading={passwordLoading}>
                Update Password
              </Button>
            </div>
          </form>
        </GlassCard>
      )}

      {activeTab === 'account' && (
        <GlassCard className="p-6">
          <h2 className="text-xl font-semibold mb-2 text-red-400">Danger Zone</h2>
          <p className="text-gray-400 mb-6">
            Once you delete your account, there is no going back. Please be certain.
          </p>

          {!showDeleteConfirm ? (
            <Button
              variant="danger"
              onClick={() => setShowDeleteConfirm(true)}
              className="border border-red-500/30"
            >
              <AlertTriangle size={18} />
              Delete My Account
            </Button>
          ) : (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-2 text-red-300">Are you absolutely sure?</h3>
              <p className="text-gray-400 mb-6">
                This action cannot be undone. This will permanently delete your account and remove all your data from our servers.
              </p>
              <div className="flex gap-3">
                <Button
                  variant="danger"
                  onClick={handleDeleteAccount}
                  isLoading={deleteLoading}
                  className="border-2 border-red-500"
                >
                  Yes, Delete My Account
                </Button>
                <Button
                  variant="secondary"
                  onClick={() => setShowDeleteConfirm(false)}
                  disabled={deleteLoading}
                >
                  Cancel
                </Button>
              </div>
            </div>
          )}
        </GlassCard>
      )}
    </div>
  );
};

export default Settings;
