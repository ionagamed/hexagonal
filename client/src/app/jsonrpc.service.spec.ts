import { TestBed, inject } from '@angular/core/testing';

import { JsonrpcService } from './jsonrpc.service';

describe('JsonrpcService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [JsonrpcService]
    });
  });

  it('should be created', inject([JsonrpcService], (service: JsonrpcService) => {
    expect(service).toBeTruthy();
  }));
});
