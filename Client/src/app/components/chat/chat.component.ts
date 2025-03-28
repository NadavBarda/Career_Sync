import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Msg } from 'src/app/interfaces/msg';
import { User } from 'src/app/interfaces/user';
import { HttpService } from 'src/app/services/http.service';
import { SessionService } from 'src/app/services/sessionService';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  messages: Msg[] = [];
  newMessage: string = '';
  user!: User;
  is_crawling: boolean = false;

  constructor(
    private httpService: HttpService,
    private sessionService: SessionService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.user = this.sessionService.getUserFromSession();
    this.httpService.post<any>('chat', { message: "start", username: this.user.username  }).subscribe(response => {
      const botMessage: Msg = { text: response.response, sender: 'bot', username: this.user.username };
      this.messages.push(botMessage);
    });
  }

  isLoggedIn(): boolean {
    return this.sessionService.isLoggedIn();
  }

  sendMessage() {
    if (this.newMessage.trim() !== '') {
      const userMessage: Msg = {
        text: this.newMessage.trim(),
        sender: 'user',
        username: this.user.username
      };
      this.messages.push(userMessage);
  
      this.httpService.post<any>('chat', { message: userMessage.text, username: this.user.username }).subscribe(response => {
        const botMessage: Msg = {
          text: response.response,
          sender: 'bot',
          username: this.user.username
        };
        if (botMessage.text.includes('Thank you!')) {
          this.router.navigate(['/careers-page']);
        }
        this.messages.push(botMessage);
      });
  
      this.newMessage = '';
    }
  }
  

  isUserMessage(message: Msg): boolean {
    return message.sender === 'user';
  }

  isBotMessage(message: Msg): boolean {
    return message.sender === 'bot';
  }
}