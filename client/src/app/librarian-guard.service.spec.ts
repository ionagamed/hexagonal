import { TestBed, inject } from '@angular/core/testing';

import { LibrarianGuardService } from './librarian-guard.service';

describe('LibrarianGuardService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [LibrarianGuardService]
    });
  });

  it('should be created', inject([LibrarianGuardService], (service: LibrarianGuardService) => {
    expect(service).toBeTruthy();
  }));
});
