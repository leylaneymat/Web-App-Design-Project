<template>
  <el-card class="event-card">
    <template #header>
      <div class="card-header">
        <h3>{{ event.name }}</h3>
        <div class="header-actions">
          <el-button type="text" @click="toggleLike">
            <el-icon v-if="event.isLiked">
              <StarFilled />
            </el-icon>
            <el-icon v-else>
              <Star />
            </el-icon>
            {{ event.likes || 0 }}
          </el-button>
          <el-button type="text" @click="showComments = true">
            <el-icon>
              <ChatRound />
            </el-icon>
            {{ event.comments.length || 0 }}
          </el-button>
        </div>
      </div>
    </template>
    <div class="card-content">
      <p>{{ event.description }}</p>
      <div class="ticket-list">
        <h4>Tickets</h4>
        <el-table :data="event.tickets" style="width: 100%">
          <el-table-column prop="name" label="Name" />
          <el-table-column prop="price" label="Price" />
        </el-table>
      </div>
    </div>
    <template #footer>
      <div class="card-footer">
        <el-button type="primary" @click="openTicketPurchaseDialog" :disabled="!userStore.isLoggedIn">Buy Ticket</el-button>
      </div>
    </template>

    <el-dialog v-model="showComments" title="Event Comments">
      <div class="comment-list">
        <div class="comment-header">
          <el-input class="comment-box" v-model="newComment" placeholder="Add a comment"
            :disabled="!userStore.isLoggedIn" />
          <el-button type="primary" @click="addComment" :disabled="!userStore.isLoggedIn">
            Add Comment
          </el-button>
        </div>
        <div v-for="comment in event.comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <span class="commenter">{{ comment.author }}</span>
            <span class="comment-date">{{ comment.createdAt }}</span>
          </div>
          <div class="comment-content">{{ comment.text }}</div>
        </div>
      </div>
    </el-dialog>

    <el-dialog v-model="showTicketPurchaseDialog" title="Purchase Ticket" width="500px">
      <div class="ticket-purchase-container">
        <el-form>
          <el-form-item label="Select Ticket">
            <el-select 
              v-model="selectedTicket" 
              placeholder="Choose a ticket"
              style="width: 100%"
            >
              <el-option
                v-for="ticket in event.tickets"
                :key="ticket.id"
                :label="`${ticket.name} - $${ticket.price}`"
                :value="ticket.id"
              >
                <div class="ticket-option">
                  <span>{{ ticket.name }}</span>
                  <span class="ticket-price">${{ ticket.price }}</span>
                </div>
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>

        <div class="purchase-actions">
          <el-button 
            type="primary" 
            @click="buyTicket" 
            :disabled="!selectedTicket"
          >
            Buy
          </el-button>
        </div>
      </div>
    </el-dialog>
  </el-card>
</template>

<script>
import { ref } from 'vue';
import { Star, StarFilled, ChatRound } from '@element-plus/icons-vue';
import { useUserStore } from '@/stores/userStore';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const showComments = ref(false);
    const newComment = ref('');
    const userStore = useUserStore();
    const showTicketPurchaseDialog = ref(false);
    const selectedTicket = ref(null);

    const toggleLike = async () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('Please login');
        return;
      }

      try {
        if (!props.event.isLiked) {
          const response = await axios.post(`http://localhost:8000/api/v1/events/${props.event.id}/likes/`);
          localStorage.setItem('likeObj', JSON.stringify(response.data));
        } else {
          let likeObj = JSON.parse(localStorage.getItem('likeObj'));
          await axios.delete(`http://localhost:8000/api/v1/events/${props.event.id}/likes/${likeObj.id}/`);
          localStorage.removeItem('likeObj');
        }

        props.event.isLiked = !props.event.isLiked;
        props.event.likes = (props.event.likes || 0) + (props.event.isLiked ? 1 : -1);
      } catch (error) {
        let likeObj = JSON.parse(localStorage.getItem('likeObj')) || null;

        if (!likeObj) {
          const response = await axios.get(`http://localhost:8000/api/v1/events/${props.event.id}/likes/`);
          const likes = response.data;
          likeObj = likes.find(like => like.user == userStore.user.id) || null;
        }

        await axios.delete(`http://localhost:8000/api/v1/events/${props.event.id}/likes/${likeObj.id}/`);
        props.event.likes = (props.event.likes || 0) - 1;
        localStorage.removeItem('likeObj');
      }
    };

    const addComment = async () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('Please login');
        return;
      }

      if (newComment.value.trim() === '') {
        ElMessage.warning('Please enter a comment');
        return;
      }

      try {
        const response = await axios.post(`http://localhost:8000/api/v1/events/${props.event.id}/comments/`, {
          text: newComment.value
        });
        props.event.comments.push(response.data);
        newComment.value = '';
      } catch (error) {
        ElMessage.error('Failed to add comment');
        console.error(error);
      }
    };

    const openTicketPurchaseDialog = () => {
      showTicketPurchaseDialog.value = true;
      selectedTicket.value = null;
    };

    const buyTicket = async () => {
      if (!userStore.isLoggedIn) {
        ElMessage.warning('Please login');
        return;
      }

      if (!selectedTicket.value) {
        ElMessage.warning('Please select a ticket');
        return;
      }

      try {
        const response = await axios.post(`http://localhost:8000/api/v1/users/${userStore.user.id}/purchased_tickets/`, {
          event: props.event.id,
          ticket: selectedTicket.value
        });

        ElMessage.success('Ticket purchased successfully');
        showTicketPurchaseDialog.value = false;
        selectedTicket.value = null;
      } catch (error) {
        ElMessage.error('Failed to purchase ticket');
        console.error(error);
      }
    };

    return {
      showComments,
      newComment,
      userStore,
      toggleLike,
      addComment,
      showTicketPurchaseDialog,
      selectedTicket,
      openTicketPurchaseDialog,
      buyTicket
    };
  },
  components: {
    Star,
    StarFilled,
    ChatRound
  }
}
</script>

<style scoped>
.event-card {
  width: 100%;
  max-width: 600px;
  margin-bottom: 24px;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
    'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ticket-list {
  margin-top: 16px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-list {
  max-height: 300px;
  overflow-y: auto;
}

.comment-box {
  padding-right: 1%;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.comment-item {
  padding: 12px;
  border-bottom: 1px solid #e4e7ed;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.comment-content {
  font-size: 16px;
}

.ticket-purchase-container {
  padding: 20px;
}

.ticket-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
  'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.ticket-price {
  color: #67c23a;
  font-weight: bold;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
  'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.purchase-actions {
  margin-top: 20px;
  text-align: right;
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC',
  'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}
</style>